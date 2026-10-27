const emojis = [
  {
    src: '/assets/mood-emoji-4.svg',
    face: '/assets/mood-face-4.svg',
    className: 'absolute right-[18%] top-0 size-[64px] rotate-[14deg]',
    faceClassName: 'absolute left-1/2 top-1/2 size-[52px] -translate-x-1/2 -translate-y-[35%]',
  },
  {
    src: '/assets/mood-emoji-1.svg',
    className: 'absolute right-0 top-[18%] size-[112px] rotate-[9deg]',
  },
  {
    src: '/assets/mood-emoji-2.svg',
    className: 'absolute bottom-0 right-[22%] size-[124px] -rotate-[21deg]',
  },
  {
    src: '/assets/mood-emoji-3.svg',
    face: '/assets/mood-face-3.svg',
    className: 'absolute bottom-[4%] right-0 size-[86px] rotate-[23deg]',
    faceClassName: 'absolute left-1/2 top-1/2 size-[68px] -translate-x-1/2 -translate-y-[42%]',
  },
]

export function MoodIllustration() {
  return (
    <div className="relative h-[150px] w-[210px] shrink-0 overflow-visible">
      {emojis.map((emoji) => (
        <div key={emoji.src} className={emoji.className}>
          <img alt="" className="size-full object-contain" src={emoji.src} />
          {emoji.face ? (
            <img
              alt=""
              className={`pointer-events-none ${emoji.faceClassName}`}
              src={emoji.face}
            />
          ) : null}
        </div>
      ))}
    </div>
  )
}
