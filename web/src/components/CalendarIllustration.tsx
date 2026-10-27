const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const dates = Array.from({ length: 28 }, (_, index) => index + 1)

export function CalendarIllustration() {
  return (
    <div className="relative h-[150px] w-[230px] shrink-0">
      <img
        alt=""
        className="absolute right-0 top-[8%] size-[42px] rotate-[67deg] object-contain"
        src="/assets/star-small.svg"
      />
      <img
        alt=""
        className="absolute right-[18%] top-0 size-[82px] rotate-[40deg] object-contain"
        src="/assets/star-large.svg"
      />

      <div className="absolute left-0 top-[10%] -rotate-[15deg] overflow-hidden rounded-[26px] bg-white shadow-[0_8px_24px_rgba(0,0,0,0.08)]">
        <div className="h-[45px] bg-[#ffe46b]" />
        <div className="px-3 py-2">
          <div className="mb-1 grid grid-cols-7 gap-1 text-center text-[10px] font-bold tracking-[-0.2px] text-[#3a3a3a]">
            {days.map((day) => (
              <span key={day}>{day}</span>
            ))}
          </div>
          <div className="grid grid-cols-7 gap-1 text-center text-[10px] font-bold text-[#a0a0a0]">
            {dates.map((date) => (
              <span key={date}>{date}</span>
            ))}
          </div>
        </div>
        <div className="absolute left-[18px] top-[52px] flex gap-[18px]">
          {Array.from({ length: 7 }).map((_, index) => (
            <span
              key={index}
              className="inline-block h-[30px] w-[10px] rounded-full bg-[#ff9898]"
            />
          ))}
        </div>
      </div>
    </div>
  )
}
