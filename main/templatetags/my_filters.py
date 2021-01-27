from django.template import Library
from django.utils.html import format_html
register = Library()

@register.filter

def yiwan(nums):
    nums=round(nums/10000,1)
    return nums

zd={'收盘价': 'round(obj.close,2)', '开盘价': 'round(obj.open,2)', '最高价': 'round(obj.high,2)', '最低价': 'round(obj.low,2)', '涨跌幅': "str(round(100*(obj.close-obj.preclose)/obj.close,2))+str('%')", '交易量(万)': 'int(obj.volume/10000)', '换手率': "str(round(obj.turn,2))+str('%')", '量比': 'round(obj.volume_ratio,2)', '市盈率': 'round(obj.pe,2)', '市净率': 'round(obj.pb,2)', '市销率': 'round(obj.ps,2)', '流通股本(亿)': 'str(round(obj.float_share/10000,2))', '总市值(亿)': 'round(obj.total_mv/10000,2)', '流通市值(亿)': 'round(obj.circ_mv/10000,2)', '连涨/跌天数': 'obj.jisuan.zhang', '连阳/阴天数': 'obj.jisuan.yang', '融资余额(亿)': 'round(obj.liangrong.rzye/100000000,2)', '融资净买入(万元)': 'int((obj.liangrong.rzmre-obj.liangrong.rzche)/10000)', '融券净卖出(万股)': 'round((obj.liangrong.rqmcl-obj.liangrong.rqchl)/10000,1)', '融资余额占流通市值比': "str(round((obj.liangrong.rzye/(obj.circ_mv*100)),2))+str('%')", '融资净买入占流动市值比': "str(round((obj.liangrong.rzmre-obj.liangrong.rzche)/(obj.circ_mv*10),2))+str('‰')", '融资3日净买入(万）': 'int(obj.liangrong.rzjmr3/10000)', '融资3日净买入占流通市值比': "str(round((obj.liangrong.rzjmr3/obj.circ_mv)/10,2))+str('‰')", '融资5日净买入(万）': 'int(obj.liangrong.rzjmr5/10000)', '融资5日净买入占流通市值比': "str(round((obj.liangrong.rzjmr5/obj.circ_mv)/10,2))+str('‰')", '行业': 'obj.code.gupiaomsg.industry', '东方财富网': "format_html(f'<a href=http://quote.eastmoney.com/{obj.code.gupiaomsg.dongfangcaifu}.html>点击跳转<a>')", '持股人数': 'obj.code.gupiaomsg.holdernum', '上市时间': 'obj.code.gupiaomsg.listdate', '持股人数截止时间': 'obj.code.gupiaomsg.holderenddate', '人均流通股（万股）': 'round(obj.code.gupiaomsg.holderfloat/obj.code.gupiaomsg.holdernum,2)', '人均持股金额（万）': 'round(obj.code.gupiaomsg.holdercirc/obj.code.gupiaomsg.holdernum,2)'}

@register.filter
def shuchu(obj, val):
    try:
        return eval(zd[val])
    except:
        return ''