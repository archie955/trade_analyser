import useLeagues from '../hooks/useLeagues'
import useField from '../hooks/useField'
import { useState } from 'react'
import { Button, FormControl, Input, InputLabel, Card } from '@mui/material'

const LeagueForm = () => {
    const [loading, setLoading] = useState(false)
    const { addLeague } = useLeagues()
    const leagueName = useField('text')

    const handleAddLeague = async (e) => {
        e.preventDefault()
        setLoading(true)

        const newLeague = {
            name: leagueName.value
        }

        await addLeague(newLeague)
        e.target.reset()
        setLoading(false)
    }

    return (
        <Card>
            <form onSubmit={handleAddLeague}>
                <FormControl>
                    <InputLabel htmlFor="name">Name</InputLabel>
                    <Input id="name" {...leagueName} />
                </FormControl>
                <Button variant="contained" type="submit" loading={loading} loadingPosition="end" size="medium">CREATE</Button>
            </form>
        </Card>
    )
}

export default LeagueForm