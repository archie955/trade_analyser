import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import teamService from "../services/team";

const useTeams = (league_id) => {
  const queryClient = useQueryClient();

  const result = useQuery({
    queryKey: ["teams", league_id],
    queryFn: () => teamService.getTeams(league_id),
    refetchOnWindowFocus: false,
  });

  const newTeamMutation = useMutation({
    mutationFn: (team) => teamService.createTeam(league_id, team),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["teams"] });
    },
  });

  const updateTeamMutation = useMutation({
    mutationFn: (newTeam) => teamService.updateTeam(league_id, newTeam),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["teams"] });
    },
  });

  const deleteTeamMutation = useMutation({
    mutationFn: (team_id) => teamService.deleteTeam(league_id, team_id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["teams"] });
    },
  });

  return {
    teams: result.data,
    isPending: result.isPending,
    addTeam: (team) => newTeamMutation.mutate(team),
    renameTeam: (newTeam) => updateTeamMutation.mutate(newTeam),
    deleteTeam: (team_id) => deleteTeamMutation.mutate(team_id),
  };
};

export default useTeams;
