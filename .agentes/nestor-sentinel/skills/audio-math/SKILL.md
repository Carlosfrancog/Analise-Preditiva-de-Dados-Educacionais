# Skill: Audio Math

Use para cálculos de PCM, frames, buffers, bitrate e latência.

## PCM bitrate

`bytes_per_second = sample_rate * channels * bits_per_sample / 8`

PCM 48 kHz, mono, 16-bit:

`48000 * 1 * 16 / 8 = 96000 B/s = 768 kbit/s`

## Bytes por frame

`frame_bytes = sample_rate * channels * bytes_per_sample * frame_duration_seconds`

20 ms em PCM16 mono 48 kHz:

`48000 * 1 * 2 * 0.020 = 1920 bytes`

## Duração de buffer

`duration_ms = buffer_bytes / bytes_per_second * 1000`

## Latência de fila

`queue_latency_ms = buffers_enfileirados * buffer_duration_ms`

Sempre converta alteração de buffer para milissegundos antes de concluir que é pequena.

## Latência total

`L_total = L_capture + L_buffer + L_network + L_processing + L_queue + L_playback`
