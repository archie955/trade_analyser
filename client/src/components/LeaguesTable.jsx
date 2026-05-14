import useLeagues from "../hooks/useLeagues";
import LeagueForm from "./CreateLeagueForm";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material'

const LeagueTable = () => {
    const { leagues, isPending } = useLeagues()

    if (isPending) {
        return <div>loading data...</div>
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
                        {leagues.map(league => (
                            <TableRow key={league.id}>
                                <TableCell>{league.name}</TableCell>
                                <TableCell>{league.created_at}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <LeagueForm />
        </div>
    )
}

export default LeagueTable