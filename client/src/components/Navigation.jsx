import Container from "@mui/material/Container";
import { styled } from "@mui/material/styles";

const Navigation = styled(Container)(() => ({
  width: "100%",
  height: "64px",
  backgroundColor: "#00338d",
  color: "#fff",
  display: "flex",
  flexDirection: "row",
  alignItems: "center",
  justifyContent: "end",
}));

export default Navigation;
