import TeamDetails from "../components/TeamDetails";
import { useParams } from "react-router-dom";
import useTeams from "../hooks/useTeams";

const Team = () => {
    const { league_id, id } = useParams()
    const { teams } = useTeams(parseInt(league_id))
    const team = teams.teams.find(t => t.id === parseInt(id))

    if (!team) {
        return (
            <div>
                Team not found
            </div>
        )
    }

    return (
        <div>
            <TeamDetails team={team} />
        </div>
    )
}

export default Team