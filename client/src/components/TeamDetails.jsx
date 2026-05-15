import useTeams from "../hooks/useTeams";
import useField from "../hooks/useField";
import { useState } from "react";
import { Button, Input, InputLabel, Card, FormControl } from "@mui/material";

const TeamDetails = ({ team }) => {
    const { renameTeam } = useTeams(team.league_id)
    const [loading, setLoading] = useState(false)
    const [editing, setEditing] = useState(false)
    const updatedName = useField('text')

    const handleUpdateTeam = async (e) => {
        e.preventDefault()
        setLoading(true)

        const updatedTeam = {
            ...team,
            name: updatedName.value
        }
        await renameTeam(updatedTeam)
        e.target.reset()
        setLoading(false)
    }

    return (
        <div>
            <div>
                {team.name} was created at {team.created_at}
                <Button variant="contained" type="button" onClick={() => setEditing(!editing)} size="medium">{editing ? "CANCEL" : "EDIT?"}</Button>
            </div>
            {editing && (
                <Card>
                    <form onSubmit={handleUpdateTeam}>
                        <FormControl>
                            <InputLabel htmlFor="newname">New name</InputLabel>
                            <Input id="newname" {...updatedName} />
                        </FormControl>
                        <Button variant="contained" type="submit" loading={loading} loadingPosition="end" size="medium">SUBMIT</Button>
                    </form>
                </Card>
            )}
        </div>
    )
}

export default TeamDetails