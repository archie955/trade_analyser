import TeamDetails from "../components/TeamDetails";
import { useParams } from "react-router-dom";
import useTeams from "../hooks/useTeams";
import TeamPlayerTable from "../components/TeamPlayerTable";
import AddPlayerTable from "../components/AddPlayerTable";

const Team = () => {
  const { league_id, id } = useParams();
  const { teams } = useTeams(parseInt(league_id));
  const team = teams.teams.find((t) => t.id === parseInt(id));

  if (!team) {
    return <div>Team not found</div>;
  }
  console.log(team);

  return (
    <div>
      <TeamDetails team={team} />
      <TeamPlayerTable league_id={team.league_id} team_id={team.id}/>
      <AddPlayerTable league_id={team.league_id} team_id={team.id} />
    </div>
  );
};

export default Team;
