# Skill: FFmpeg Diagnostics

Use FFprobe primeiro para descobrir o formato real. Não converta áudio apenas para "ver se resolve".

## Inspeção

```bash
ffprobe -hide_banner input.wav
```

```bash
ffprobe -v quiet -print_format json -show_format -show_streams input.wav
```

## PCM16LE 48 kHz mono

```bash
ffmpeg -i input.wav -ac 1 -ar 48000 -c:a pcm_s16le output.wav
```

## PCM RAW

```bash
ffmpeg -i input.wav -f s16le -acodec pcm_s16le -ac 1 -ar 48000 output.pcm
```

## Reprodução RAW

```bash
ffplay -f s16le -ar 48000 -ac 1 output.pcm
```

## Silêncio

```bash
ffmpeg -i input.wav -af silencedetect=noise=-40dB:d=0.4 -f null -
```

## Estatísticas

```bash
ffmpeg -i input.wav -af astats=metadata=1:reset=1 -f null -
```

## Loudness

```bash
ffmpeg -i input.wav -af loudnorm=print_format=json -f null -
```
