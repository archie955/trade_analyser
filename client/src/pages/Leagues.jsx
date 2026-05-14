import { Breadcrumbs, Link } from "@mui/material";
import Navigation from "../components/Navigation";
import LeagueTable from "../components/LeaguesTable";

const Leagues = () => {
    return (
        <div>
            <Navigation>
                <Breadcrumbs aria-label="breadcumb" color={'#fff'}>
                    <Link underline="hover" color="inherit" href="/" sx={{font: 'IBM Plex Mono', fontSize: '1.5em'}}>
                        Login
                    </Link>
                    <Link underline="hover" color="inherit" href="/leagues" sx={{fontSize: '1.5em'}}>
                        Leagues
                    </Link>
                </Breadcrumbs>
            </Navigation>
            <LeagueTable />
        </div>
    )
}

export default Leagues