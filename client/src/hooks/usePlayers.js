import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query";
import getPlayers from "../services/players";

const usePlayers = ({
  league_id,
  free_agent = false,
  pos = null,
  team = null,
  asc = false,
  skip = null,
  limit = null,
}) => {
  const queryClient = useQueryClient();

  const result = useQuery({
    queryKey: ["players", league_id, free_agent, pos, team, asc, skip, limit],
    queryFn: () =>
      getPlayers(league_id, free_agent, pos, team, asc, skip, limit),
    refetchOnWindowFocus: false,
  });

  const removeFromFA = useMutation({
    mutationFn: (id) => {
      const players = queryClient.getQueryData(["players"]);
      queryClient.setQueryData(
        ["players"],
        players.filter((p) => p.id !== id),
      );
    },
  });

  return {
    players: result.data,
    isPending: result.isPending,
    remove: (id) => removeFromFA.mutate(id),
  };
};

export default usePlayers;
