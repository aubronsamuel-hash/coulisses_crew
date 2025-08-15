import { useState, useCallback } from 'react';
import * as missionService from '../services/missions';

interface Mission {
  id: number;
  [key: string]: unknown;
}

export function useMissions(token: string | null) {
  const [missions, setMissions] = useState<Mission[]>([]);

  const load = useCallback(async () => {
    if (!token) return;
    const data = await missionService.list(token);
    setMissions(data);
  }, [token]);

  const createMission = useCallback(
    async (mission: Record<string, unknown>) => {
      if (!token) return;
      const created = await missionService.create(token, mission);
      setMissions((m) => [...m, created]);
    },
    [token]
  );

  const updateMission = useCallback(
    async (id: number, mission: Record<string, unknown>) => {
      if (!token) return;
      const updated = await missionService.update(token, id, mission);
      setMissions((m) => m.map((mi) => (mi.id === id ? updated : mi)));
    },
    [token]
  );

  const deleteMission = useCallback(
    async (id: number) => {
      if (!token) return;
      await missionService.remove(token, id);
      setMissions((m) => m.filter((mi) => mi.id !== id));
    },
    [token]
  );

  const assignMission = useCallback(
    async (id: number, userId: number) => {
      if (!token) return;
      const updated = await missionService.assign(token, id, userId);
      setMissions((m) => m.map((mi) => (mi.id === id ? updated : mi)));
    },
    [token]
  );

  return { missions, load, createMission, updateMission, deleteMission, assignMission };
}
