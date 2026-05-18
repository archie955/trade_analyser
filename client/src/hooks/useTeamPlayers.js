import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import teamPlayerService from "../services/teamplayers";

const useTeamPlayers = (league_id, team_id) => {
  const queryClient = useQueryClient();

  const result = useQuery({
    queryKey: ["teamplayers", league_id, team_id],
    queryFn: () => teamPlayerService.getTeamPlayers(league_id, team_id),
    refetchOnWindowFocus: false,
  });

  const newTeamPlayerMutation = useMutation({
    mutationFn: (player_id) =>
      teamPlayerService.addTeamPlayer(league_id, team_id, player_id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["teamplayers"] });
    },
  });

  const removeTeamPlayerMutation = useMutation({
    mutationFn: (player_id) =>
      teamPlayerService.removeTeamPlayers(league_id, team_id, player_id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["teamplayers"] });
    },
  });

  return {
    teamPlayers: result.data,
    isPending: result.isPending,
    addPlayer: (player_id) => newTeamPlayerMutation.mutate(player_id),
    removePlayer: (player_id) => removeTeamPlayerMutation.mutate(player_id),
  };
};

export default useTeamPlayers;
