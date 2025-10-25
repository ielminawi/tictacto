import {
  ControlBar,
  GridLayout,
  ParticipantTile,
  RoomAudioRenderer,
  useTracks,
  RoomContext,
} from '@livekit/components-react';
import { Room, Track } from 'livekit-client';
import '@livekit/components-styles';
import { useEffect, useState } from 'react';

const serverUrl = 'wss://tactohackathon-k8al281m.livekit.cloud';

// ⚠️ Replace this hardcoded token later with one fetched dynamically from your Python token server.
const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiZGVidWciLCJ2aWRlbyI6eyJyb29tSm9pbiI6dHJ1ZSwicm9vbSI6ImdhbGFjdGFjdG9jdXMtcm9vbSIsImNhblB1Ymxpc2giOnRydWUsImNhblN1YnNjcmliZSI6dHJ1ZSwiY2FuUHVibGlzaERhdGEiOnRydWV9LCJzdWIiOiJkZWJ1ZyIsImlzcyI6IkFQSXVOWUVLR3lMbVMzcSIsIm5iZiI6MTc2MTQzMTg0NiwiZXhwIjoxNzYxNDUzNDQ2fQ.LeO78NFjvOVcazdvKLixOm6Y5fQ6g_Uhu80lSbUyABA';

export default function App() {
  const [room] = useState(() => new Room({
    adaptiveStream: true,
    dynacast: true,
  }));

  useEffect(() => {
    let mounted = true;
    const connect = async () => {
      if (mounted) {
        try {
          await room.connect(serverUrl, token);
          console.log('✅ Connected to room:', room.name);
        } catch (err) {
          console.error('❌ Connection failed:', err);
        }
      }
    };
    connect();

    return () => {
      mounted = false;
      room.disconnect();
    };
  }, [room]);

  return (
    <RoomContext.Provider value={room}>
      <div data-lk-theme="default" style={{ height: '100vh' }}>
        <MyVideoConference />
        <RoomAudioRenderer />
        <ControlBar />
      </div>
    </RoomContext.Provider>
  );
}

function MyVideoConference() {
  const tracks = useTracks(
    [
      { source: Track.Source.Camera, withPlaceholder: true },
      { source: Track.Source.ScreenShare, withPlaceholder: false },
    ],
    { onlySubscribed: false },
  );

  return (
    <GridLayout
      tracks={tracks}
      style={{ height: 'calc(100vh - var(--lk-control-bar-height))' }}
    >
      <ParticipantTile />
    </GridLayout>
  );
}
