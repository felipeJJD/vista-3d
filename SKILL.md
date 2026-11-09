---
name: vista-3d
description: Gera um app web 3D de "escolha seu lugar vendo a vista antes de reservar" para qualquer negócio com lugares marcados — restaurante com palco, bar com show, cinema, teatro, auditório, casa de eventos. Mapa 3D visto de cima, toque na mesa ou poltrona, a câmera voa até a vista daquele lugar e mostra distância, ângulo e preço, com reserva. Use quando o usuário pedir "ver a vista da mesa/poltrona", mapa de lugares 3D, reserva com visualização, ou o app de cinema que viralizou adaptado para um negócio. Também grava o modo demo em MP4 1080x1920 para Reels.
---

# vista-3d — escolha o lugar vendo a vista

Um arquivo HTML só (`assets/vista-3d.html`), Three.js 0.160 via CDN, bloom, sem build. Abre no celular e no navegador.

## 1. Gerar para um negócio

1. Copie `assets/vista-3d.html` para a pasta do projeto (ex.: `restaurante.html`).
2. Troque **só** o bloco `window.VENUE` no topo:
   - `name`, `subtitle`, `times` (horários; o 2º campo é a etiqueta, ex. `"SHOW"`), `timeOn`.
   - `unit`: "Mesa", "Poltrona", "Lugar". `currency`.
   - `focus`: o que se olha (`w`, `d`, `h` do palco, `z` do centro, `sign` = letreiro neon).
   - `room`: largura, fundo, altura, cor da parede e do piso.
   - `zones`: nome, preço e cor de cada setor. A **primeira** zona ganha a cor de destaque no mapa.
   - `rows` (z de cada fileira + zona) e `cols` (x de cada coluna): a grade de mesas, numeradas por fileira.
   - `seats` por mesa, `taken` (ocupadas, aparecem com pessoas sentadas), `demo` (2 mesas livres que o modo demo escolhe).
3. Mantenha 3 m entre colunas e 2,5 m entre fileiras; primeira fileira a ≥ 3 m da borda do palco.

## 2. Ver e testar

Sirva a pasta (`python -m http.server`) e abra no navegador. `?demo` roda o roteiro sozinho:
toca na mesa `demo[0]`, voa até a vista, abre o card, volta ao mapa, toca em `demo[1]`, reserva.

## 3. Gravar para Reels

```
python scripts/capture.py restaurante.html app.mp4 --secs 16      # 1080x1920, 30 fps, relógio manual
python scripts/capture.py restaurante.html teste/t.mp4 --only 0,75,130,300,450   # só quadros soltos para conferir
```

Usa o Chrome instalado (`channel="chrome"`). Câmera, card e toque animam pelo mesmo relógio, então o vídeo sai liso
mesmo se o render for lento. Confira uma folha de contato antes de editar.

## Cuidados

- O texto do card e os rótulos vêm do `VENUE`: revise acentos e preços.
- Não use marca ou nome de um negócio real sem autorização; prefira um nome inventado no vídeo.
