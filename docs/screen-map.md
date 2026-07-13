# Peta Layar & State Machine

Sumber kebenaran: `src/moodin_interface/core/state_machine.py`.

## Alur utama

splash -> idleMirror -> (onboarding) -> mainMenu -> capture -> result -> trends/mainMenu

## Transisi legal

| Dari | Ke |
|------|-----|
| splash | idleMirror, onboarding |
| idleMirror | onboarding, mainMenu |
| onboarding | mainMenu, idleMirror |
| mainMenu | capture, trends, settings, idleMirror |
| capture | result, mainMenu, idleMirror |
| result | mainMenu, trends, capture, idleMirror |
| trends | mainMenu, idleMirror |
| settings | mainMenu, idleMirror |

## Aturan idle

Idle timer (default 45 dtk, dari app_config.yaml) memindahkan UI kembali ke
`idleMirror` bila tidak ada interaksi. Nonaktif di splash & idleMirror.

## Kondisi khusus (ditangani inline, belum jadi layar terpisah)

- LowLight / NoFace / WeakSignal -> ditampilkan di CaptureScreen via `qualityMessage`.
- Offline (broker terputus) -> tombol "Deteksi Mood" dinonaktifkan di MainMenu.
