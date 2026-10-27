export function Mascot() {
  return (
    <div className="pointer-events-none relative h-[220px] w-[280px] shrink-0">
      <img
        alt=""
        className="absolute bottom-0 left-[18%] h-[32px] w-[228px] max-w-none object-contain"
        src="/assets/mascot-shadow.svg"
      />

      <div className="absolute left-[18%] top-[8%] -rotate-[16deg]">
        <div className="relative h-[106px] w-[154px] rounded-[10px] bg-gradient-to-br from-[#3a3a3a] to-[#ff9898] p-[5px] shadow-[inset_0_0_8px_rgba(0,0,0,0.25)]">
          <div className="h-full w-full rounded-[9px] bg-gradient-to-br from-white via-[#ffe46b] to-[#ab911f]" />
        </div>
        <img
          alt=""
          className="absolute left-1/2 top-[28%] h-[65px] w-[115px] -translate-x-1/2 object-contain"
          src="/assets/mascot-face.svg"
        />
      </div>

      <img
        alt=""
        className="absolute bottom-[18%] right-[8%] h-[84px] w-[86px] rotate-[3deg] object-contain"
        src="/assets/mascot-arm-right.svg"
      />
      <img
        alt=""
        className="absolute bottom-[14%] left-[8%] h-[72px] w-[86px] -scale-y-100 rotate-[164deg] object-contain"
        src="/assets/mascot-arm-left.svg"
      />
      <img
        alt=""
        className="absolute bottom-[8%] right-[18%] h-[59px] w-[61px] -rotate-[16deg] object-contain"
        src="/assets/mascot-leg-right.svg"
      />
      <img
        alt=""
        className="absolute bottom-[2%] left-[2%] h-[59px] w-[61px] rotate-[142deg] object-contain"
        src="/assets/mascot-leg-left.svg"
      />
    </div>
  )
}
