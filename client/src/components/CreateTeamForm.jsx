import useTeams from '../hooks/useTeams'
import useField from '../hooks/useField'
import { useState } from 'react'
import { Button, FormControl, Input, InputLabel, Card } from '@mui/material'

const TeamForm = ({ id }) => {
  const [loading, setLoading] = useState(false)
  const { addTeam } = useTeams(id)
  const teamName = useField('text')

  const handleAddTeam = async (e) => {
    e.preventDefault()
    setLoading(true)

    const newTeam = {
      name: teamName.value
    }

    await addTeam(newTeam)
    e.target.reset()
    setLoading(false)
  }

  return (
    <Card>
      <form onSubmit={handleAddTeam}>
        <FormControl>
          <InputLabel htmlFor="name">Name</InputLabel>
          <Input id="name" {...teamName} />
        </FormControl>
        <Button variant="contained" type="submit" loading={loading} loadingPosition="end" size="medium">CREATE</Button>
      </form>
    </Card>
  )
}

export default TeamForm