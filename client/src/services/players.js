import api from "./api";

const getPlayers = async (
  league_id,
  free_agent = false,
  pos = null,
  team = null,
  asc = false,
  skip = null,
  limit = null,
) => {
  const params = {};
  if (free_agent) {
    params.free_agent = true;
  }
  if (pos !== null) {
    params.pos = pos;
  }
  if (team !== null) {
    params.team = team;
  }
  if (asc) {
    params.asc = asc;
  }
  if (skip !== null) {
    params.skip = skip;
  }
  if (limit !== null) {
    params.limit = limit;
  }

  const response = await api.get(`/players/${league_id}`, { params });
  return response.data;
};

export default getPlayers;
