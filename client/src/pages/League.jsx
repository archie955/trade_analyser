import LeagueDetails from '../components/LeagueDetails'
import { useParams } from 'react-router-dom'
import useLeagues from '../hooks/useLeagues'

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
        <LeagueDetails league={league}/>
    )
}

export default League