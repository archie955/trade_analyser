import api from "./api";

const getTeamPlayers = async (league_id, team_id) => {
  const response = await api.get(
    `/leagues/${league_id}/teams/${team_id}/players`,
  );
  return response.data;
};

const addTeamPlayers = async (league_id, team_id, player_id) => {
  console.log(
    `Endpoint successfully called, attempting to add player ${player_id}`,
  );
  const response = await api.post(
    `/leagues/${league_id}/teams/${team_id}/players`,
    { id: player_id },
  );
  return response.data;
};

const removeTeamPlayers = async (league_id, team_id, player_id) => {
  await api.delete(
    `/leagues/${league_id}/teams/${team_id}/players/${player_id}`,
  );
};

export default { getTeamPlayers, addTeamPlayers, removeTeamPlayers };
