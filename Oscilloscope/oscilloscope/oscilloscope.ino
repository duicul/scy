#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h>
#include <stdio.h>
#define USART_BAUDRATE 9600
#define BAUD_PRESCALE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1) 

uint16_t i=0,del_time=100,inc=3;
uint16_t samples=100;
uint16_t settings[10][10],setting_ind=0;


void UART_init()
{ cli();
  UCSR0B=0;
  UCSR0A=0;
  UCSR0C |=  (1 << UCSZ00) | (1 << UCSZ01);/* Use 8-bit char size */
  
  UBRR0L = BAUD_PRESCALE;      /* Load lower 8-bits of the baud rate */
  UBRR0H = (BAUD_PRESCALE >> 8);   /* Load upper 8-bits*/
  
  UCSR0B |= (1 << RXCIE0)|(1 << RXEN0) | (1 << TXEN0); /* Turn on transmission and reception (1 << RXCIE0)*/
  sei();
}

void USART_Flush(void)
{
  unsigned char dummy;
  while (UCSR0A & (1<<RXC0)) dummy = UDR0;
  //PORTB^=(1<<5);
}

unsigned char UART_RxChar()
{ //USART_Flush();
  while (!(UCSR0A & (1 << RXC0)));/* Wait till data is received */
  PORTB^=(1<<5);
  return(UDR0);    /* Return the byte */
}

void UART_TxChar(char ch)
{ while (! (UCSR0A & (1<<UDRE0)));  /* Wait for empty transmit buffer */
  PORTB^=(1<<5);
  UDR0 = ch ;
}

ISR(USART_RX_vect)//USART_RX_vect
{ char ReceivedByte;
  ReceivedByte=UDR0;
  UDR0=ReceivedByte;
  PORTB^=(1<<5);
}


void setup() {
  DDRB|=(1<<5);
  PORTB&=~(1<<5);
  UART_init();
  //UART_TxChar('2');
}

void loop() {
  //UART_TxChar(UART_RxChar());
  //PORTB^=(1<<5);
  /*PORTB^=(1<<5);
  delay(del_time);
  del_time-=inc;
  inc=(del_time<10||del_time>100)?(-inc):inc;*/
    
}
