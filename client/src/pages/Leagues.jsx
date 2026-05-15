import { Breadcrumbs } from "@mui/material";
import { Link } from "react-router-dom";
import Navigation from "../components/Navigation";
import LeagueTable from "../components/LeaguesTable";

const Leagues = () => {
  return (
    <div>
      <Navigation>
        <Breadcrumbs aria-label="breadcumb" color={"#fff"}>
          <Link to="/">Login</Link>
          <Link to="/leagues">Leagues</Link>
          <Link to="/home">Home</Link>
        </Breadcrumbs>
      </Navigation>
      <LeagueTable />
    </div>
  );
};

export default Leagues;
