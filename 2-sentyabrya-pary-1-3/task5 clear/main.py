class Figure:
    coords = (0,0)
    width = 1
    color = 'Оранжевый'

fig = Figure()

fig2 = Figure()
fig2.coords = (5,5)
fig2.width = 10
fig2.color = 'Бордовый'

for figname, f in (('fig', fig), ('fig2',fig2)):
    print(f'Фигура {figname}, координаты: {f.coords}, ширина: {f.width}, цвет: {f.color}')




