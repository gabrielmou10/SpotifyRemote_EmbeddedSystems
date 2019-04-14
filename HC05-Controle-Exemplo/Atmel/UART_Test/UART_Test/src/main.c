/**
* - TODO [x] Botao A -> callback
* - TODO [x] Botao B -> callback
* - TODO [x] Botao C -> callback
* - TODO [X] Incluir ADC - reproduizr outro codigo
* - TODO [X] enviar ADC bluetooth
* - TODO [ ] saidas
* - TODO [ ]   - LED
* - TODO [ ]   - Buzzer
*/


/************************************************************************/
/* includes                                                             */
/************************************************************************/
#include <asf.h>
#include <string.h>

/************************************************************************/
/* defines                                                              */
/************************************************************************/
#ifdef DEBUG_SERIAL
#define UART_COMM USART1
#else
#define UART_COMM USART0
#endif

//PB2 - play/pause - butA
#define BUTA_PIO          PIOB
#define BUTA_PIO_ID        11
#define BUTA_PIO_IDX       2u
#define BUTA_PIO_IDX_MASK  (1u << BUTA_PIO_IDX)

//PA3 - next - butB
#define BUTB_PIO           PIOA
#define BUTB_PIO_ID        10
#define BUTB_PIO_IDX       3u
#define BUTB_PIO_IDX_MASK  (1u << BUTB_PIO_IDX)

//PA4 - previous - butC
#define BUTC_PIO           PIOA
#define BUTC_PIO_ID        10
#define BUTC_PIO_IDX       4u
#define BUTC_PIO_IDX_MASK  (1u << BUTC_PIO_IDX)

//PA19 - BUZZER
#define BUZZER_PIO           PIOA
#define BUZZER_PIO_ID        10
#define BUZZER_PIO_IDX       19u
#define BUZZER_PIO_IDX_MASK  (1u << BUZZER_PIO_IDX)

/** Reference voltage for AFEC,in mv. */
#define VOLT_REF        (3300)
/** The maximal digital value */
/** 2^12 - 1                  */
#define MAX_DIGITAL     (4095)

//potenciometro
#define ANALOG_CHANNEL				 2

/************************************************************************/
/* constants                                                            */
/************************************************************************/

/************************************************************************/
/* variaveis globais                                                    */
/************************************************************************/
volatile Bool butA_flag;
volatile Bool butB_flag;
volatile Bool butC_flag;

volatile bool g_is_conversion_done_analog = false;
volatile uint32_t g_ul_value_analog = 0;

volatile long g_systimer = 0;

/* Canal do sensor de temperatura */
#define AFEC_CHANNEL_TEMP_SENSOR 11

/************************************************************************/
/* handler / callbacks                                                  */
/************************************************************************/
void butA_callback(void){
	butA_flag = true;
}
void butB_callback(void){
	butB_flag = true;
}
void butC_callback(void){
	butC_flag = true;
}
static void AFEC_Pot_callback(void)
{
	g_ul_value_analog = afec_channel_get_value(AFEC0, ANALOG_CHANNEL);
	g_is_conversion_done_analog = true;
}
void SysTick_Handler() {
	g_systimer++;
}
void TC1_Handler(void){
	volatile uint32_t ul_dummy;
	ul_dummy = tc_get_status(TC0, 1);

	UNUSED(ul_dummy);

	afec_channel_enable(AFEC0, ANALOG_CHANNEL);

	afec_start_software_conversion(AFEC0);
	
}

/************************************************************************/
/* prototypes                                                           */
/************************************************************************/
void TC_init(Tc * TC, int ID_TC, int TC_CHANNEL, int freq);

/************************************************************************/
/* interrupcoes                                                         */
/************************************************************************/

/************************************************************************/
/* funcoes                                                              */
/************************************************************************/
void config_console(void) {
	usart_serial_options_t config;
	config.baudrate = 9600;
	config.charlength = US_MR_CHRL_8_BIT;
	config.paritytype = US_MR_PAR_NO;
	config.stopbits = false;
	usart_serial_init(USART1, &config);
	usart_enable_tx(USART1);
	usart_enable_rx(USART1);
}

void usart_put_string(Usart *usart, char str[]) {
	usart_serial_write_packet(usart, str, strlen(str));
}

int usart_get_string(Usart *usart, char buffer[], int bufferlen, int timeout_ms) {
	long timestart = g_systimer;
	uint32_t rx;
	uint32_t counter = 0;
	
	while(g_systimer - timestart < timeout_ms && counter < bufferlen - 1) {
		if(usart_read(usart, &rx) == 0) {
			//timestart = g_systimer; // reset timeout
			buffer[counter++] = rx;
		}
	}
	buffer[counter] = 0x00;
	return counter;
}

void usart_send_command(Usart *usart, char buffer_rx[], int bufferlen, char buffer_tx[], int timeout) {
	usart_put_string(usart, buffer_tx);
	usart_get_string(usart, buffer_rx, bufferlen, timeout);
}

void usart_log(char* name, char* log) {
	usart_put_string(USART1, "[");
	usart_put_string(USART1, name);
	usart_put_string(USART1, "] ");
	usart_put_string(USART1, log);
	usart_put_string(USART1, "\r\n");
}

void hc05_config_server(void) {
	usart_serial_options_t config;
	config.baudrate = 9600;
	config.charlength = US_MR_CHRL_8_BIT;
	config.paritytype = US_MR_PAR_NO;
	config.stopbits = false;
	usart_serial_init(USART0, &config);
	usart_enable_tx(USART0);
	usart_enable_rx(USART0);
	
	// RX - PB0  TX - PB1
	pio_configure(PIOB, PIO_PERIPH_C, (1 << 0), PIO_DEFAULT);
	pio_configure(PIOB, PIO_PERIPH_C, (1 << 1), PIO_DEFAULT);
}

int hc05_server_init(void) {
	char buffer_rx[128];
	usart_send_command(USART0, buffer_rx, 1000, "AT", 1000);
	usart_send_command(USART0, buffer_rx, 1000, "AT", 1000);
	usart_send_command(USART0, buffer_rx, 1000, "AT+NAMEeli", 1000);
	usart_log("hc05_server_init", buffer_rx);
	usart_send_command(USART0, buffer_rx, 1000, "AT", 1000);
	usart_send_command(USART0, buffer_rx, 1000, "AT+PIN0000", 1000);
	usart_log("hc05_server_init", buffer_rx);
}

static void config_ADC_VOLUME(void){
	
	afec_enable(AFEC0);
	struct afec_config afec_cfg;
	afec_get_config_defaults(&afec_cfg);
	afec_init(AFEC0, &afec_cfg);
	afec_set_trigger(AFEC0, AFEC_TRIG_SW);
	afec_set_callback(AFEC0, AFEC_INTERRUPT_EOC_2,	AFEC_Pot_callback, 1);

	struct afec_ch_config afec_ch_cfg;
	afec_ch_get_config_defaults(&afec_ch_cfg);
	afec_ch_cfg.gain = AFEC_GAINVALUE_0;
	afec_ch_set_config(AFEC0, AFEC_CHANNEL_TEMP_SENSOR, &afec_ch_cfg);
	afec_ch_set_config(AFEC0, ANALOG_CHANNEL, &afec_ch_cfg);

	afec_channel_set_analog_offset(AFEC0, ANALOG_CHANNEL, 0x200);
	
	afec_channel_enable(AFEC0, ANALOG_CHANNEL);
}

void TC_init(Tc * TC, int ID_TC, int TC_CHANNEL, int freq){
	uint32_t ul_div;
	uint32_t ul_tcclks;
	uint32_t ul_sysclk = sysclk_get_cpu_hz();

	uint32_t channel = 1;
	pmc_enable_periph_clk(ID_TC);

	/** Configura o TC para operar em  4Mhz e interrupçcão no RC compare */
	tc_find_mck_divisor(freq, ul_sysclk, &ul_div, &ul_tcclks, ul_sysclk);
	tc_init(TC, TC_CHANNEL, ul_tcclks | TC_CMR_CPCTRG);
	tc_write_rc(TC, TC_CHANNEL, (ul_sysclk / ul_div) / freq);

	/* Configura e ativa interrupçcão no TC canal 0 */
	/* Interrupção no C */
	NVIC_EnableIRQ((IRQn_Type) ID_TC);
	tc_enable_interrupt(TC, TC_CHANNEL, TC_IER_CPCS);

	/* Inicializa o canal 0 do TC */
	tc_start(TC, TC_CHANNEL);
}

void io_init(void){
	// Inicializa clock do periférico PIO responsavel pelo botao
	pmc_enable_periph_clk(BUTB_PIO_ID);
	pmc_enable_periph_clk(BUTC_PIO_ID);
	pmc_enable_periph_clk(BUTA_PIO_ID);
	
	// Configura PIO para lidar com o pino do botão como entrada
	// com pull-up
	pio_configure(BUTA_PIO, PIO_INPUT, BUTA_PIO_IDX_MASK, PIO_PULLUP);
	pio_configure(BUTB_PIO, PIO_INPUT, BUTB_PIO_IDX_MASK, PIO_PULLUP);
	pio_configure(BUTC_PIO, PIO_INPUT, BUTC_PIO_IDX_MASK, PIO_PULLUP);
	pio_set_output(BUZZER_PIO, BUZZER_PIO_IDX_MASK, 0, 0, 0);
	
	// Configura interrupção no pino referente ao botao e associa
	// função de callback caso uma interrupção for gerada
	// a função de callback é a: but_callback()
	pio_handler_set(BUTA_PIO, BUTA_PIO_ID, BUTA_PIO_IDX_MASK, PIO_IT_RISE_EDGE, butA_callback);
	pio_handler_set(BUTB_PIO, BUTB_PIO_ID, BUTB_PIO_IDX_MASK, PIO_IT_RISE_EDGE, butB_callback);
	pio_handler_set(BUTC_PIO, BUTC_PIO_ID, BUTC_PIO_IDX_MASK, PIO_IT_RISE_EDGE, butC_callback);
	
	// Ativa interrupção
	pio_enable_interrupt(BUTA_PIO, BUTA_PIO_IDX_MASK);
	pio_enable_interrupt(BUTB_PIO, BUTB_PIO_IDX_MASK);
	pio_enable_interrupt(BUTC_PIO, BUTC_PIO_IDX_MASK);

	// Configura NVIC para receber interrupcoes do PIO do botao
	// com prioridade 4 (quanto mais próximo de 0 maior)
	NVIC_EnableIRQ(BUTA_PIO_ID);
	NVIC_EnableIRQ(BUTB_PIO_ID);
	NVIC_SetPriority(BUTA_PIO_ID, 4); // Prioridade 4
	NVIC_SetPriority(BUTB_PIO_ID, 4); // Prioridade 4
}

void send_command(char msg[]){
	char eof = 'X';
	while(!usart_is_tx_ready(UART_COMM));
	usart_write(UART_COMM, msg[0]);
	while(!usart_is_tx_ready(UART_COMM));
	usart_write(UART_COMM, eof);
}

static int convert_adc_to_volume(int32_t ADC_value){
	int32_t ul_vol;
	int32_t ul_pot;
	int32_t ul_volume;
	//converte bits -> tensão (Volts) -> Volume(0-16)
	ul_vol = ADC_value * VOLT_REF / (float) MAX_DIGITAL;
	ul_volume = (16 * (ul_vol) - 300) / 3270;
	
	return(ul_volume);
}

/************************************************************************/
/* Main                                                                 */
/************************************************************************/
int main (void)
{
	board_init();
	sysclk_init();
	ioport_init();
	delay_init();
	SysTick_Config(sysclk_get_cpu_hz() / 1000); // 1 ms
	config_console();
	io_init();
	
	char *codigos[17] = {"D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"};
	
	// Desativa watchdog
	WDT->WDT_MR = WDT_MR_WDDIS;
	
	TC_init(TC0, ID_TC1, 1, 0.5);
	
	/* inicializa delay */
	delay_init(sysclk_get_cpu_hz());

	/* inicializa e configura adc */
	config_ADC_VOLUME();
	
	/* incializa conversão ADC */
	afec_start_software_conversion(AFEC0);
	
	
	#ifndef DEBUG_SERIAL
	usart_put_string(USART1, "Inicializando...\r\n");
	usart_put_string(USART1, "Config HC05 Server...\r\n");
	hc05_config_server();
	hc05_server_init();
	#endif
	
	
	while(1) {
		
		
		if(g_is_conversion_done_analog == true) {
			g_is_conversion_done_analog = false;
			//sprintf(volume, "%d", );
			send_command(codigos[convert_adc_to_volume(g_ul_value_analog)]);
		}
		if(butA_flag){
			pio_set(BUZZER_PIO, BUZZER_PIO_IDX_MASK);
			delay_ms(60);
			pio_clear(BUZZER_PIO, BUZZER_PIO_IDX_MASK);
			send_command("A");
			butA_flag = false;
		}
		if(butB_flag){
			pio_set(BUZZER_PIO, BUZZER_PIO_IDX_MASK);
			delay_ms(60);
			pio_clear(BUZZER_PIO, BUZZER_PIO_IDX_MASK);
			send_command("B");
			butB_flag = false;
		}
		if(butC_flag){
			pio_set(BUZZER_PIO, BUZZER_PIO_IDX_MASK);
			delay_ms(50);
			pio_clear(BUZZER_PIO, BUZZER_PIO_IDX_MASK);
			send_command("C");
			butC_flag = false;
		}

		delay_s(0.3);
	}
}
