import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from queue import Queue

token = '7131803241:AAEGJ64L06ubYcOZRapBLm1AAPsGYxvj_Vw'

# Função para calcular o valor líquido
def calcular_valor_liquido(update, context):
    try:
        # Obtenha as informações do usuário
        posto_graduacao = update.message.text.split()[0]
        qtd_dias = int(update.message.text.split()[1])

        # Tabela de soldos
        soldos = {
            "CMG": 11451.00,
            "CF": 11250.00,
            "CC": 11088.00,
            "CT": 9135.00,
            "1ºTEN": 8245.00,
            "2ºTEN": 7490.00,
            "SO": 6169.00,
            "1ºSG": 5483.00,
            "2ºSG": 4770.00,
            "3ºSG": 3825.00,
            "CB": 2627.00,
            "SD": 1800.00
        }

        # Obtenha o soldo com base na escolha do usuário
        soldo = soldos[posto_graduacao]

        # Cálculo da Gratificação Representativa de Operações (Grat Rep Op)
        grat_rep_op = soldo * 0.02

        # Determinação da alíquota de Imposto de Renda
        if soldo <= 2826.66:
            aliquota_ir = 0
        elif 2826.66 < soldo <= 3751.05:
            aliquota_ir = 0.15
        elif 3751.06 < soldo <= 4664.68:
            aliquota_ir = 0.225
        else:
            aliquota_ir = 0.275

        # Cálculo do Total da Gratificação Representativa de Operações
        total_grat_rep_op = grat_rep_op * qtd_dias

        # Cálculo do Desconto de Imposto de Renda
        desconto_ir = total_grat_rep_op * aliquota_ir

        # Cálculo do Total a Receber
        total_a_receber = total_grat_rep_op - desconto_ir

        # Exibição dos resultados
        update.message.reply_text(f"RELATÓRIO\n\nPosto/Grad: {posto_graduacao}\nSoldo: R$ {soldo:.2f}\nGratRepOp por dia: R$ {grat_rep_op:.2f}\nQuantidade de dias: {qtd_dias}\nTotal GratRepOp: R$ {total_grat_rep_op:.2f}\nDesconto Imposto de Renda ({aliquota_ir * 100:.1f}%): - R$ {desconto_ir:.2f}\nValor líquido a receber: R$ {total_a_receber:.2f}")
    except (ValueError, IndexError):
        update.message.reply_text("Por favor, insira valores válidos no formato: 'Posto/Graduação Quantidade de dias'")

updater = Updater(token, update_queue=Queue())
dispatcher = updater.get_dispatcher()

calcular_valor_liquido_handler = CommandHandler('calcular', calcular_valor_liquido)
message_handler = MessageHandler(Filters.text & ~Filters.command, calcular_valor_liquido)

dispatcher.add_handler(calcular_valor_liquido_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()