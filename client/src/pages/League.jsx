import LeagueDetails from '../components/LeagueDetails'
import { useParams } from 'react-router-dom'
import useLeagues from '../hooks/useLeagues'
import TeamTable from '../components/TeamsTable'
import TeamForm from '../components/CreateTeamForm'

const League = () => {
  const { id } = useParams()
  const { leagues } = useLeagues()
  const league = leagues.leagues.find(l => l.id === parseInt(id))

  if (!league) {
    return (
      <div>
                League not found
      </div>
    )
  }

  return (
    <div>
      <LeagueDetails league={league} />
      <TeamTable id={league.id} />
      <TeamForm id={league.id} />
    </div>
  )
}

export default League