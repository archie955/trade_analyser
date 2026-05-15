import useTeams from "../hooks/useTeams";
import { useState } from "react"
import { 
    Table, TableBody, TableCell,
    TableContainer, TableHead,
    TableRow, Paper, Button } from '@mui/material'
import { Link } from "react-router-dom"

const TeamTable = ({ id }) => {
    const { teams, isPending, deleteTeam } = useTeams(id)
    const [loading, setLoading] = useState(false)

    if (isPending) {
        return <div>loading data...</div>
    }

    if (teams.teams.length === 0) {
        return (
            <div>
                <div>No teams yet</div>
            </div>
        )
    }

    const handleDeleteTeam = async (team_id) => {
        setLoading(true)
        await deleteTeam(team_id)
        setLoading(false)
    }

    return (
        <div>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>name</TableCell>
                            <TableCell>created at</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {teams.teams.map(team => (
                            <TableRow key={team.id}>
                                <TableCell>
                                    <Link to={`/leagues/${team.league_id}/${team.id}`}>
                                        {team.name}
                                    </Link>
                                </TableCell>
                                <TableCell>{team.created_at}</TableCell>
                                <TableCell><Button variant="contained" type="button" onClick={() => handleDeleteTeam(team.league_id, team.id)} loading={loading} loadingPosition="end" size="medium">DELETE</Button></TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    )
}

export default TeamTable