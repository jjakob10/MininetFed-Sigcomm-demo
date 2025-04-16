#!/usr/bin/env python

import sys
import threading
import time
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.energy import Energy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
import warnings
warnings.filterwarnings("ignore", message=".*Matplotlib GUI outside of the main thread.*")

# Configurações visuais
battery_width = 0.1
battery_height = 0.3
battery_head_height = 0.05
battery_head_width = battery_width * 0.375
nivel_maximo = 0.000003  # Em Wh, igual ao battery_capacity do sensor1

# Posições dos nós
nodos = [
    (1.1, 0.590),
    (1.828, 0.705),
    (3.41, 0.705),
    (3.93, 0.590),
    (4.73, 0.705),
    (6.43, 0.475),
    (7.76, 0.610),
    (8.36, 0.705),
    (9.8, 0.610),
    (10.44, 0.59),
    (11.02, 0.5),
]

def iniciar_plot(sensores,titulo="Monitoring System"):
    img = mpimg.imread('planta.png')
    fig, ax = plt.subplots(figsize=(12, 3), num=titulo)
    ax.imshow(img, extent=[0, 12, 0, 3])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3)
    ax.set_title(titulo)
    ax.axis('off')

    barras_nivel = []
    sensor_map = {}  # sensor -> (barra, y, text)

    for i, sensor in enumerate(sensores):
        x, y = nodos[i]

        # Corpo da bateria
        corpo = patches.Rectangle((x - battery_width / 2, y), battery_width, battery_height,
                                  edgecolor='black', facecolor='none', lw=1.5)
        ax.add_patch(corpo)

        # Cabeça
        cabeca = patches.Rectangle((x - battery_head_width / 2, y + battery_height),
                                   battery_head_width, battery_head_height, color='black')
        ax.add_patch(cabeca)

        # Barra de nível
        barra = patches.Rectangle((x - battery_width / 2 + 0.02, y),
                                  battery_width - 0.04, battery_height,
                                  color='green')
        ax.add_patch(barra)
        barras_nivel.append(barra)

        # Texto de porcentagem
        text = ax.text(x + 0.02, y + battery_height + 0.15, "100%", ha='center', va='bottom', fontsize=12)
        sensor_map[sensor] = (barra, y, text)

    def update(frame):
        for sensor in sensores:
            barra, base_y, text = sensor_map[sensor]
            consumo = getattr(sensor, 'consumption', 0)
            battery_capacity = getattr(sensor, 'battery_capacity', 0.000003)

            carga = max(0.0, min(1.0, 1 - (consumo / battery_capacity)))
            altura = carga * battery_height
            barra.set_height(altura)
            barra.set_y(base_y)

            # Atualiza a cor da barra
            if carga > 0.6:
                barra.set_color('green')
            elif carga > 0.3:
                barra.set_color('orange')
            else:
                barra.set_color('red')

            # Atualiza o texto de porcentagem
            percentage = int(carga * 100)
            text.set_text(f"{percentage}%")
            text.set_y(base_y + battery_height + 0.15)

        return list(barras_nivel) + [text for _, _, text in sensor_map.values()]

    ani = FuncAnimation(fig, update, interval=1000)
    plt.show()

def topology(args):
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    s1 = net.addSensor('sensor1', ip6='2001::1/64', voltage=3.7, battery_capacity=0.000003, panid='0xbeef')
    s2 = net.addSensor('sensor2', ip6='2001::2/64', voltage=3.7, battery_capacity=0.000003, panid='0xbeef')
    s3 = net.addSensor('sensor3', ip6='2001::3/64', voltage=3.7, battery_capacity=0.000003, panid='0xbeef')
    s4 = net.addSensor('sensor4', ip6='2001::4/64', voltage=3.7, battery_capacity=0.000003, panid='0xbeef')
    s5 = net.addSensor('sensor5', ip6='2001::5/64', voltage=3.7, battery_capacity=0.000003, panid='0xbeef')
    s6 = net.addSensor('sensor6', ip6='2001::6/64', voltage=3.7, battery_capacity=0.000003, panid='0xbeef')
    s7 = net.addSensor('sensor7', ip6='2001::7/64', voltage=3.7, battery_capacity=0.000003, panid='0xbeef')
    s8 = net.addSensor('sensor8', ip6='2001::8/64', voltage=3.7, battery_capacity=0.000003, panid='0xbeef')
    s9 = net.addSensor('sensor9', ip6='2001::9/64', voltage=3.7, battery_capacity=0.000003, panid='0xbeef')
    s10 = net.addSensor('sensor10', ip6='2001::10/64', voltage=3.7, battery_capacity=0.000003, panid='0xbeef')
    s11 = net.addSensor('sensor11', ip6='2001::11/64', voltage=3.7, battery_capacity=0.000003, panid='0xbeef')

    sensores = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11]

    info("*** Configuring nodes\n")
    net.configureNodes()

    if '-p' in args:
        thread_energy = threading.Thread(
        target=lambda: net.plotEnergyMonitor(nodes=net.sensors, title="Battery Consumptions"),
        daemon=True
        )
        thread_energy.start()
        #net.plotEnergyMonitor(nodes=net.sensors, title="Battery Consumptions")

    info("*** Starting network\n")
    net.build()

    info("*** Measuring energy consumption\n")
    Energy(sensores)

    # Inicia o gráfico numa thread
    thread_plot = threading.Thread(target=iniciar_plot, args=(sensores,), daemon=True)
    thread_plot.start()

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
