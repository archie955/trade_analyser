import { useQuery } from "@tanstack/react-query";
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
  const result = useQuery({
    queryKey: ["players", league_id, free_agent, pos, team, asc, skip, limit],
    queryFn: () =>
      getPlayers(league_id, free_agent, pos, team, asc, skip, limit),
    refetchOnWindowFocus: false,
  });

  return {
    players: result.data,
    isPending: result.isPending,
  };
};

export default usePlayers;
