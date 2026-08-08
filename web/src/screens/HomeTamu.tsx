import React from 'react';
import { ActionButton } from '../components/ActionButton';
import { MoodIllustration } from '../components/MoodIllustration';
import { CalendarIllustration } from '../components/CalendarIllustration';
import { Mascot } from '../components/Mascot';

export const HomeTamu: React.FC = () => {
  return (
    <div
      style={{
        position: 'relative',
        width: 600,
        height: 1024,
        background: 'linear-gradient(18.93deg, var(--bg-grad-start) 0%, var(--bg-grad-end) 51.1%, var(--bg-grad-end) 100%)',
        overflow: 'hidden',
        fontFamily: 'sans-serif'
      }}
    >
      {/* AVATAR TAMU */}
      <div style={{ position: 'absolute', left: 514.35 - 32.72, top: 60.22 - 32.72, width: 32.72 * 2, height: 32.72 * 2, borderRadius: '50%', backgroundColor: 'var(--success)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <span style={{ color: 'var(--text-primary)', fontSize: 32, fontWeight: 'bold' }}>?</span>
      </div>
      <div style={{ position: 'absolute', top: 60.22 + 32.72 + 8, width: 600, textAlign: 'right', paddingRight: 600 - (514.35 + 32.72), color: 'var(--text-secondary)', fontSize: 16 }}>
        Daftar lewat aplikasi MoodIn
      </div>

      {/* SAPAAN */}
      <div style={{ position: 'absolute', left: 55.44, top: 118 }}>
        <div style={{ fontSize: 56, fontWeight: 'bold', color: 'var(--text-primary)', lineHeight: 1 }}>Halo, User!</div>
        <div style={{ fontSize: 20, color: 'var(--text-secondary)', marginTop: 8 }}>Apa yang ingin kamu lakukan hari ini?</div>
      </div>

      {/* KARTU 1: Deteksi Mood */}
      <div style={{ position: 'absolute', left: 55.44, top: 256.264, width: 491.631, height: 182.297, backgroundColor: 'var(--danger)', borderRadius: 28.48 }}>
        <div style={{ padding: '32px 24px', position: 'relative', zIndex: 10 }}>
          <div style={{ fontSize: 32, fontWeight: 'bold', color: 'var(--text-primary)', lineHeight: 1.2, width: '60%' }}>
            Deteksi<br/>Mood
          </div>
          <div style={{ fontSize: 20, color: 'var(--text-primary)', marginTop: 12 }}>
            Deteksi moodmu sekarang!
          </div>
        </div>
        <MoodIllustration />
      </div>

      {/* KARTU 2: Tren 7 Hari */}
      <div style={{ position: 'absolute', left: 55.44, top: 471.555, width: 491.631, height: 182.297, backgroundColor: 'var(--primary)', borderRadius: 28.48 }}>
        <div style={{ padding: '32px 24px', position: 'relative', zIndex: 10, textAlign: 'right' }}>
          <div style={{ fontSize: 32, fontWeight: 'bold', color: 'var(--text-primary)', lineHeight: 1.2 }}>
            Tren<br/>7 Hari
          </div>
          <div style={{ fontSize: 20, color: 'var(--text-primary)', marginTop: 12 }}>
            Lihat tren mingguanmu!
          </div>
        </div>
        <CalendarIllustration />
      </div>

      {/* DUA TOMBOL BAWAH */}
      <ActionButton x={55.4399} y={707.195} width={215.02} height={94.5867} text="Pengaturan" />
      <ActionButton x={55.4399} y={819.38} width={215.02} height={94.5867} text="Kembali" />

      {/* MASKOT */}
      <Mascot />
    </div>
  );
};
