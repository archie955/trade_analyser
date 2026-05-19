import useTeamPlayers from "../hooks/useTeamPlayers";
import usePlayers from "../hooks/usePlayers";
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

const AddPlayerTable = ({ league_id, team_id }) => {
  const { players, isPending, remove } = usePlayers({
    league_id: league_id,
    limit: 30,
  });
  const { addPlayer } = useTeamPlayers(league_id, team_id);
  const [loading, setLoading] = useState(false);

  if (isPending) {
    return <div>loading data...</div>;
  }

  const handleAddPlayer = async (player_id) => {
    setLoading(true);
    await addPlayer(player_id);
    remove(player_id);
    setLoading(false);
  };

  return (
    <div>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Team</TableCell>
              <TableCell>Position</TableCell>
              <TableCell>Points/Week</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {players.players.map((player) => (
              <TableRow key={player.id}>
                <TableCell>{player.name}</TableCell>
                <TableCell>{player.team}</TableCell>
                <TableCell>{player.position}</TableCell>
                <TableCell>{player.points_ppr}</TableCell>
                <TableCell>
                  <Button
                    variant="contained"
                    type="button"
                    onClick={() => handleAddPlayer(player.id)}
                    loading={loading}
                    loadingPosition="end"
                    size="medium"
                  >
                    ADD
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default AddPlayerTable;
