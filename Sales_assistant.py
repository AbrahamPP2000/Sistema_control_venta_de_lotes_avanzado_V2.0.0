import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import logging
import json


class ConversationContext:
    def __init__(self):
        self.current_topic: str = ""
        self.last_lot_mentioned: Optional[Tuple[int, int]] = None  # (manzana, lote)
        self.last_payment_method: Optional[str] = None
        self.conversation_history: List[Dict[str, str]] = []
        self.user_preferences: Dict[str, Any] = {}


class LotSalesAssistant:
    def __init__(self):
        # Configuración de logging
        logging.basicConfig(
            filename='chatbot.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('SalesAssistant')

        # Inicialización de la conexión
        try:
            from Data_Import_and_processing import get_connection
            self.connection = get_connection()
            self.cursor = self.connection.cursor()
            self.logger.info("Conexión a la base de datos establecida exitosamente")
        except Exception as e:
            self.logger.error(f"Error al conectar a la base de datos: {str(e)}")
            raise

        # Contexto de la conversación
        self.context = ConversationContext()

        # Configuración de intenciones y respuestas
        self._setup_intents()
        self._setup_detailed_responses()

    def _setup_intents(self):
        """Configuración detallada de intenciones y palabras clave"""
        self.intent_patterns = {
            'consulta_lotes': {
                'keywords': ['disponible', 'hay', 'tienen', 'lote', 'precio', 'costo', 'cuanto', 'metros', 'tamaño'],
                'patterns': [
                    r'lote (\d+)',
                    r'manzana (\d+)',
                    r'(\d+) metros'
                ]
            },
            'consulta_pagos': {
                'keywords': ['pago', 'precio', 'anticipo', 'mensualidad', 'parcialidad', 'contado', 'financiamiento'],
                'subcategories': {
                    'contado': ['contado', 'único', 'completo', 'total'],
                    'parcialidades': ['mensualidad', 'parcialidad', 'plazo', 'anticipo'],
                    'especie': ['especie', 'intercambio', 'trueque']
                }
            },
            'proceso_compra': {
                'keywords': ['comprar', 'proceso', 'documentos', 'requisitos', 'necesito', 'pasos'],
                'stages': ['selección', 'pago', 'documentación', 'contrato', 'entrega']
            },
            'consulta_estado': {
                'keywords': ['estado', 'estatus', 'avance', 'progreso'],
                'patterns': [r'estado (del )?lote (\d+)']
            }
        }

    def _setup_detailed_responses(self):
        """Configuración de respuestas detalladas por categoría"""
        self.detailed_responses = {
            'pago_contado': {
                'description': self._get_contado_info,
                'beneficios': self._get_contado_benefits,
                'requisitos': self._get_contado_requirements
            },
            'pago_parcialidades': {
                'description': self._get_parcialidades_info,
                'planes': self._get_payment_plans,
                'requisitos': self._get_parcialidades_requirements
            },
            'pago_especie': {
                'description': self._get_especie_info,
                'proceso': self._get_especie_process,
                'requisitos': self._get_especie_requirements
            }
        }

    def _get_contado_info(self) -> str:
        """Obtiene información detallada sobre pago de contado"""
        try:
            query = "SELECT ValorDescuento FROM ConfiguracionPagos WHERE TipoPago = 'Contado' LIMIT 1"
            self.cursor.execute(query)
            descuento = self.cursor.fetchone()

            descuento_actual = descuento[0] if descuento else 10  # Valor por defecto

            return f"""
            Pago de Contado:
            - Pago único del valor total del lote
            - Descuento actual del {descuento_actual}% sobre el precio total
            - Escrituración inmediata
            - Sin cargos adicionales

            Beneficios adicionales:
            - Proceso más rápido
            - Menor documentación requerida
            - Prioridad en la selección de lotes
            """
        except Exception as e:
            self.logger.error(f"Error al obtener información de pago de contado: {str(e)}")
            return "Lo siento, hubo un error al consultar la información de pago de contado."

    def _get_contado_benefits(self) -> str:
        """Beneficios del pago de contado"""
        return """
        Beneficios del Pago de Contado:
        - Descuento significativo sobre el precio total
        - Escrituración inmediata
        - Proceso simplificado
        - Sin revisión de historial crediticio
        """

    def _get_contado_requirements(self) -> str:
        """Requisitos para pago de contado"""
        return """
        Requisitos para Pago de Contado:
        - Identificación oficial vigente
        - Comprobante de domicilio reciente
        - Forma de pago válida
        """

    def _get_parcialidades_info(self) -> str:
        """Obtiene información detallada sobre pago en parcialidades"""
        try:
            query = """
                SELECT PorcentajeMinimo, PlazoMaximo, TasaInteres 
                FROM ConfiguracionPagos 
                WHERE TipoPago = 'Parcialidades' 
                LIMIT 1
            """
            self.cursor.execute(query)
            config = self.cursor.fetchone()

            if config:
                porcentaje_minimo, plazo_maximo, tasa_interes = config
                return f"""
                Pago en Parcialidades:
                - Anticipo mínimo del {porcentaje_minimo}%
                - Plazo hasta {plazo_maximo} meses
                - Tasa de interés anual del {tasa_interes}%

                Planes disponibles:
                1. Plan Flexible:
                   - Ajuste de mensualidades según capacidad
                   - Posibilidad de pagos adicionales

                2. Plan Fijo:
                   - Mensualidades fijas
                   - Sin cargos por adelanto de pagos
                """
            else:
                return "Información sobre parcialidades no disponible en este momento."
        except Exception as e:
            self.logger.error(f"Error al obtener información de parcialidades: {str(e)}")
            return "Lo siento, hubo un error al consultar la información de parcialidades."

    def _get_parcialidades_requirements(self) -> str:
        """Requisitos para pago en parcialidades"""
        return """
        Requisitos para Pago en Parcialidades:
        - Identificación oficial vigente
        - Comprobante de domicilio reciente
        - Comprobante de ingresos
        - Referencias personales
        """

    def _get_payment_plans(self) -> str:
        """Obtiene los planes de pago disponibles"""
        try:
            query = "SELECT * FROM PlanesPago WHERE Activo = 1"
            self.cursor.execute(query)
            planes = self.cursor.fetchall()

            if not planes:
                return "No hay planes de pago registrados actualmente."

            response = "Planes de pago disponibles:\n\n"
            for plan in planes:
                response += f"""
                Plan: {plan[1]}
                - Plazo: {plan[2]} meses
                - Tasa de interés: {plan[3]}%
                - Anticipo mínimo: {plan[4]}%
                """
            return response
        except Exception as e:
            self.logger.error(f"Error al obtener planes de pago: {str(e)}")
            return "Error al consultar los planes de pago."

    def _get_especie_info(self) -> str:
        """Información sobre pago en especie"""
        return """
        Pago en Especie:

        1. Características:
           - Intercambio de bienes por el valor del lote
           - Evaluación del bien ofrecido
           - Proceso de peritaje incluido

        2. Bienes aceptados:
           - Vehículos recientes
           - Maquinaria industrial
           - Otros bienes inmuebles
           - Mercancía comercial

        3. Proceso:
           - Presentación del bien
           - Evaluación y peritaje
           - Determinación de valor
           - Formalización del intercambio

        ¿Desea conocer más detalles sobre algún aspecto?
        """

    def _get_especie_process(self) -> str:
        """Proceso detallado de pago en especie"""
        return """
        Proceso de Pago en Especie:

        1. Evaluación Inicial:
           - Descripción detallada del bien
           - Documentación de propiedad
           - Fotografías o inspección inicial

        2. Peritaje:
           - Evaluación por perito certificado
           - Determinación de valor comercial
           - Informe técnico detallado

        3. Negociación:
           - Comparación con valor del lote
           - Acuerdo de diferencias (si aplica)
           - Términos de intercambio

        4. Formalización:
           - Contratos de permuta
           - Documentación legal
           - Transferencia de propiedad
        """

    def _get_especie_requirements(self) -> str:
        """Requisitos para pago en especie"""
        return """
        Requisitos para Pago en Especie:

        1. Documentación del Bien:
           - Factura original o documento de propiedad
           - Comprobante de no adeudos
           - Verificación vehicular (si aplica)

        2. Documentación Personal:
           - Identificación oficial
           - Comprobante de domicilio
           - RFC activo

        3. Condiciones del Bien:
           - Buen estado general
           - Libre de gravámenes
           - Valor comparable al lote
        """

    def _get_available_lots(self, filters: Dict = None) -> str:
        """Obtiene información detallada de lotes disponibles con filtros opcionales"""
        try:
            # Consulta simplificada que solo usa los campos que sabemos que existen
            base_query = """
                SELECT NoLote, NoManzana, MtsCuadrados, PrecioTotal 
                FROM Lotes 
                WHERE Estatus = 'Disponible'
                LIMIT 5
            """

            self.cursor.execute(base_query)
            lots = self.cursor.fetchall()

            if not lots:
                return "No hay lotes disponibles en este momento."

            response = "Lotes disponibles:\n\n"
            for lot in lots:
                response += f"""
                Lote {lot[0]} Manzana {lot[1]}:
                - Superficie: {lot[2]}m²
                - Precio Total: ${lot[3]:,.2f}
                """
            return response
        except Exception as e:
            self.logger.error(f"Error al consultar lotes disponibles: {str(e)}")
            return "Lo siento, hubo un error al consultar los lotes disponibles."

    def _get_lot_details(self, manzana: int, lote: int) -> str:
        """Obtiene detalles específicos de un lote"""
        try:
            query = """
                SELECT l.*, 
                       (SELECT GROUP_CONCAT(s.Nombre) FROM Servicios s 
                        JOIN LotesServicios ls ON s.IdServicio = ls.IdServicio 
                        WHERE ls.NoLote = l.NoLote AND ls.NoManzana = l.NoManzana) as Servicios
                FROM Lotes l
                WHERE l.NoManzana = %s AND l.NoLote = %s
            """
            self.cursor.execute(query, (manzana, lote))
            lot_info = self.cursor.fetchone()

            if not lot_info:
                return f"No se encontró información del lote {lote} en la manzana {manzana}."

            return f"""
            Información detallada del lote:

            Ubicación:
            - Manzana: {lot_info[0]}
            - Lote: {lot_info[1]}
            - Dirección: {lot_info[2]}

            Características:
            - Superficie: {lot_info[3]}m²
            - Precio por m²: ${lot_info[4]:,.2f}
            - Precio total: ${lot_info[5]:,.2f}

            Estado: {lot_info[6]}
            Servicios disponibles: {lot_info[7] or 'No hay información de servicios'}
            """
        except Exception as e:
            self.logger.error(f"Error al obtener detalles del lote: {str(e)}")
            return "Error al consultar los detalles del lote."

    def process_query(self, user_input: str) -> str:
        """Procesa la consulta del usuario y genera una respuesta contextual"""
        try:
            # Guardar la consulta en el historial
            self.context.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user_input': user_input
            })

            # Identificar números de lote o manzana mencionados
            lot_matches = re.findall(r'lote (\d+)', user_input.lower())
            manzana_matches = re.findall(r'manzana (\d+)', user_input.lower())

            if lot_matches and manzana_matches:
                self.context.last_lot_mentioned = (int(manzana_matches[0]), int(lot_matches[0]))
                return self._get_lot_details(int(manzana_matches[0]), int(lot_matches[0]))

            # Procesar consultas sobre pagos
            for payment_type, keywords in self.intent_patterns['consulta_pagos']['subcategories'].items():
                if any(keyword in user_input.lower() for keyword in keywords):
                    self.context.last_payment_method = payment_type
                    if payment_type == 'contado':
                        return self._get_contado_info()
                    elif payment_type == 'parcialidades':
                        return self._get_parcialidades_info()
                    elif payment_type == 'especie':
                        return self._get_especie_info()

            # Procesar consultas sobre lotes disponibles
            if any(keyword in user_input.lower() for keyword in self.intent_patterns['consulta_lotes']['keywords']):
                return self._get_available_lots()

            # Procesar consultas sobre el proceso de compra
            if any(keyword in user_input.lower() for keyword in self.intent_patterns['proceso_compra']['keywords']):
                return """
                Proceso de Compra:

                1. Selección del Lote
                   - Revisión de disponibilidad
                   - Verificación de medidas y ubicación

                2. Análisis Financiero
                   - Evaluación de opciones de pago
                   - Cálculo de mensualidades (si aplica)

                3. Documentación Requerida
                   - Identificación oficial
                   - Comprobante de domicilio
                   - Comprobante de ingresos (para parcialidades)

                4. Formalización
                   - Firma de contrato
                   - Pago inicial o anticipo

                5. Seguimiento
                   - Entrega de recibos
                   - Actualización de estado de cuenta

                ¿Desea información detallada sobre alguna etapa específica?
                """

            # Si no se identificó una intención clara, dar una respuesta general
            return """
            Puedo ayudarte con:

            1. Información de lotes disponibles
               - Ver lotes específicos (ejemplo: "muestra lote 5 manzana 3")
               - Búsqueda por características (ejemplo: "lotes de más de 200m²")

            2. Opciones de pago
               - Pago de contado
               - Planes de financiamiento
               - Pago en especie

            3. Proceso de compra
               - Requisitos
               - Documentación
               - Pasos a seguir

            ¿Qué información te gustaría conocer?
            """
        except Exception as e:
            self.logger.error(f"Error procesando consulta: {str(e)}")
            return "Lo siento, hubo un error al procesar tu consulta. ¿Podrías intentar de nuevo?"

    def chat(self):
        """Inicia una sesión de chat interactiva mejorada"""
        print("\n¡Bienvenido al Asistente Virtual de Ventas de Lotes!")
        print("\nPuedo ayudarte con:")
        print("1. Consulta de lotes disponibles")
        print("2. Información de precios y medidas")
        print("3. Opciones de financiamiento")
        print("4. Proceso de compra")
        print("5. Requisitos y documentación")
        print("\nPuedes escribir tu pregunta naturalmente o usar estas opciones:")
        print("- Ver lotes: 'muestra lotes disponibles'")
        print("- Pagos: 'opciones de pago'")
        print("- Proceso: 'cómo comprar un lote'")
        print("\nEscribe 'salir' cuando desees terminar.")

        while True:
            try:
                user_input = input("\nTú: ").lower()
                if user_input == 'salir':
                    print("\nGracias por tu interés. ¡Hasta pronto!")
                    # Guardar el historial de la conversación antes de salir
                    self._save_conversation_history()
                    break

                response = self.process_query(user_input)
                print(f"\nAsistente: {response}")

            except Exception as e:
                self.logger.error(f"Error en el chat: {str(e)}")
                print("\nAsistente: Lo siento, hubo un error. ¿Podrías reformular tu pregunta?")

    def _save_conversation_history(self):
        """Guarda el historial de la conversación en un archivo JSON"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_history_{timestamp}.json"

            history_data = {
                'session_id': timestamp,
                'conversation': self.context.conversation_history,
                'user_preferences': self.context.user_preferences
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=2)

            self.logger.info(f"Historial de conversación guardado en {filename}")
        except Exception as e:
            self.logger.error(f"Error al guardar el historial: {str(e)}")


if __name__ == "__main__":
    assistant = LotSalesAssistant()
    assistant.chat()