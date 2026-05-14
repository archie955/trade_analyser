import api from "./api"

const baseUrl = "/leagues"

const getLeagues = async () => {
    const response = await api.get(baseUrl)
    return response.data
}

const createLeague = async (name) => {
    const response = await api.post(baseUrl, name)
    return response.data
}

const updateLeague = async (updatedLeague) => {
    const response = await api.put(baseUrl, updatedLeague)
    return response.data
}

const deleteLeague = async (id) => {
    await api.delete(`${baseUrl}/${id}`)
}

export default { getLeagues, createLeague, updateLeague, deleteLeague }