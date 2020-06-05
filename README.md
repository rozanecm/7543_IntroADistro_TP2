# General
Para ver el enunciado, [click aquí](enunciado.pdf).

# Setup
La cátedra proveerá el framework a través del siguiente repositorio: [https://github.com/7543distrofiuba/tp2-sockets](https://github.com/7543distrofiuba/tp2-sockets).

La herramienta comcast para simular distintas condiciones de la red esta disponible en la siguiente página web: [https://github.com/tylertreat/comcast](https://github.com/tylertreat/comcast).

[Aquí](README_framework.md) está disponible el archivo README correspondiente al framework dado por la cátedra.

## Corriendo comcast...
Para correr `comcast` hubo que utilizar los siguientes comandos:

```
~/go/bin/comcast -device=lo --packet-loss=10%
~/go/bin/comcast --stop -device=lo
```

# Informe
El informe se redacta en [Google docs](https://docs.google.com/document/d/1q0q5_-lDr0N07dROPfxd0CdPBd4SWc8seS3IEiPc3sI/edit?usp=sharing).
