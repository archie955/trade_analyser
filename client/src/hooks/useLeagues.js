import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import leagueService from "../services/league";

const useLeagues = () => {
  const queryClient = useQueryClient();

  const result = useQuery({
    queryKey: ["leagues"],
    queryFn: leagueService.getLeagues,
    refetchOnWindowFocus: false,
  });

  const newLeagueMutation = useMutation({
    mutationFn: leagueService.createLeague,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["leagues"] });
    },
  });

  const updateLeagueMutation = useMutation({
    mutationFn: leagueService.updateLeague,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["leagues"] });
    },
  });

  const deleteLeagueMutation = useMutation({
    mutationFn: leagueService.deleteLeague,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["leagues"] });
    },
  });

  return {
    leagues: result.data,
    isPending: result.isPending,
    addLeague: (league) => newLeagueMutation.mutate(league),
    renameLeague: (league) => updateLeagueMutation.mutate({ ...league }),
    deleteLeague: (id) => deleteLeagueMutation.mutate(id),
  };
};

export default useLeagues;
