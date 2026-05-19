import useTeamPlayers from "../hooks/useTeamPlayers";
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

const TeamPlayerTable = ({ league_id, team_id }) => {
  const { teamPlayers, isPending, removePlayer } = useTeamPlayers(
    league_id,
    team_id,
  );
  const [loading, setLoading] = useState(false);

  if (isPending) {
    return <div>loading data...</div>;
  }

  if (teamPlayers.players.length === 0) {
    return (
      <div>
        <div>No players yet</div>
      </div>
    );
  }

  const handleRemovePlayer = async (player_id) => {
    setLoading(true);
    await removePlayer(player_id);
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
            {teamPlayers.players.map((player) => (
              <TableRow key={player.id}>
                <TableCell>{player.name}</TableCell>
                <TableCell>{player.team}</TableCell>
                <TableCell>{player.position}</TableCell>
                <TableCell>{player.points_ppr}</TableCell>
                <TableCell>
                  <Button
                    variant="contained"
                    type="button"
                    onClick={() => handleRemovePlayer(player.id)}
                    loading={loading}
                    loadingPosition="end"
                    size="medium"
                  >
                    REMOVE
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

export default TeamPlayerTable;
