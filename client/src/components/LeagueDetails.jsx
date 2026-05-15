import useLeagues from '../hooks/useLeagues'
import useField from '../hooks/useField'
import { useState } from 'react'
import { Button, Input, InputLabel, Card, FormControl } from '@mui/material'

const LeagueDetails = ({ league }) => {
  const { renameLeague } = useLeagues()
  const [loading, setLoading] = useState(false)
  const [editing, setEditing] = useState(false)
  const updatedName = useField('text')

  const handleUpdateLeague = async (e) => {
    e.preventDefault()
    setLoading(true)

    const updatedLeague = {
      ...league,
      name: updatedName.value
    }
    await renameLeague(updatedLeague)
    e.target.reset()
    setLoading(false)
  }

  return (
    <div>
      <div>
        {league.name} was created at {league.created_at}
        <Button variant="contained" type="button" onClick={() => setEditing(!editing)} size="medium">{editing ? 'CANCEL' : 'EDIT?'}</Button>
      </div>
      {editing && (
        <Card>
          <form onSubmit={handleUpdateLeague}>
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

export default LeagueDetails