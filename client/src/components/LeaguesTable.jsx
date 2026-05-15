import useLeagues from "../hooks/useLeagues";
import LeagueForm from "./CreateLeagueForm";
import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
} from "@mui/material";
import { Link } from "react-router-dom";

const LeagueTable = () => {
  const { leagues, isPending, deleteLeague } = useLeagues();
  const [loading, setLoading] = useState(false);

  if (isPending) {
    return <div>loading data...</div>;
  }

  if (leagues.leagues.length === 0) {
    return (
      <div>
        <div>No leagues yet...</div>
        <LeagueForm />
      </div>
    );
  }

  const handleDeleteLeague = async (id) => {
    setLoading(true);
    await deleteLeague(id);
    setLoading(false);
  };

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
            {leagues.leagues.map((league) => (
              <TableRow key={league.id}>
                <TableCell>
                  <Link to={`/leagues/${league.id}`}>{league.name}</Link>
                </TableCell>
                <TableCell>{league.created_at}</TableCell>
                <TableCell>
                  <Button
                    variant="contained"
                    type="button"
                    onClick={() => handleDeleteLeague(league.id)}
                    loading={loading}
                    loadingPosition="end"
                    size="medium"
                  >
                    DELETE
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <LeagueForm />
    </div>
  );
};

export default LeagueTable;
