
from django.utils import simplejson

def percentage(value, total):
    if total == 0:
        return 0
    return (value * 100) /float(total)

def social_reach_graph(facebook, twitter, gplus, linkedin, foursquare):
    
    f_per, f_count = facebook
    l_per, l_count = linkedin
    g_per, g_count = gplus
    t_per, t_count = twitter
    fq_per, fq_count = foursquare
    
    data = []
    if f_count:    
        f_obj = {
                  "percentage": f_per,
                  "color": '#D44B5F',
                  "text": '{}'.format(f_count),
                  "x": 150,
                  "y": 130,
                  "image": {
                    "path": '/static/img/iconos/1_face.png',
                    "width": '26',
                    "height": '20',
                    "offsetx": '-13',
                    "offsety": '-20',
                  }
                }
        data.append(f_obj)
    if t_count:
        t_obj = {
                  "percentage": t_per,
                  "color": '#FF834F',
                  "text": '{}'.format(t_count),
                  "x": 150,
                  "y": 170,
                  "image": {
                    "path": '/static/img/iconos/6_twitter.png',
                    "width": '26',
                    "height": '20',
                    "offsetx": '-13',
                    "offsety": '-20'
                  }
                }
        data.append(t_obj)
    if l_count:
        l_obj = {
                  "percentage": l_per,
                  "color": '#DC6666',
                  "text": '{}'.format(l_count),
                  "x": 150,
                  "y": 150,
                  "image": {
                    "path": '/static/img/iconos/3_linke.png',
                    "width": '26',
                    "height": '20',
                    "offsetx": '-13',
                    "offsety": '-20'
                  }
                }
        data.append(l_obj)
    
    if g_count:
        g_obj = {
                  "percentage": g_per,
                  "color": '#D44B66',
                  "text": '{}'.format(g_count),
                  "x": 150,
                  "y": 110,
                  "image": {
                    "path": '/static/img/iconos/4_mail.png',
                    "width": '26',
                    "height": '20',
                    "offsetx": '-13',
                    "offsety": '-20'
                  }
                }
        data.append(g_obj)
    
    if fq_count:
        fq_obj = {
                  "percentage": fq_per,
                  "color": '#FF834F',
                  "text": '{}'.format(fq_count),
                  "x": 150,
                  "y": 190,
                  "image": {
                    "path": '/static/img/iconos/2_four.png',
                    "width": '26',
                    "height": '20',
                    "offsetx": '-13',
                    "offsety": '-20'
                  }
                }
        data.append(fq_obj)


    
    return simplejson.dumps(data)