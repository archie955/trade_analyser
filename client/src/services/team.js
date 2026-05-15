import api from "./api";

const getTeams = async (id) => {
  const response = await api.get(`/leagues/${id}/teams`);
  return response.data;
};

const createTeam = async (id, name) => {
  console.log(name);
  const response = await api.post(`/leagues/${id}/teams`, name);
  return response.data;
};

const updateTeam = async (id, updatedTeam) => {
  const response = await api.put(`/leagues/${id}/teams`, updatedTeam);
  return response.data;
};

const deleteTeam = async (league_id, id) => {
  await api.delete(`/leagues/${league_id}/teams/${id}`);
};

export default { getTeams, createTeam, updateTeam, deleteTeam };
