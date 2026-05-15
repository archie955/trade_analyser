import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import teamService from '../services/team'

const useTeams = (id) => {
    const queryClient = useQueryClient()

    const result = useQuery({
        queryKey: ['teams'],
        queryFn: () => teamService.getTeams(id),
        refetchOnWindowFocus: false
    })

    const newTeamMutation = useMutation({
        mutationFn: (team) => teamService.createTeam(id, team),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['teams'] })
        }
    })

    const updateTeamMutation = useMutation({
        mutationFn: (newTeam) => teamService.updateTeam(id, newTeam),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['teams'] })
        }
    })

    const deleteTeamMutation = useMutation({
        mutationFn: (team_id) => teamService.deleteTeam(id, team_id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['teams'] })
        }
    })

    return {
        teams: result.data,
        isPending: result.isPending,
        addTeam: (team) => newTeamMutation.mutate(team),
        renameTeam: (newTeam) => updateTeamMutation.mutate(newTeam),
        deleteTeam: (team_id) => deleteTeamMutation.mutate(team_id)
    }
}

export default useTeams