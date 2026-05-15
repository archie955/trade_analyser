import styled from "styled-components";

const Button = styled.button`
  background: #00338d;
  font-size: 1em;
  margin: 1em;
  color: #fff;
  padding: 0.25em 1em;
  border: 2px solid black;
  border-radius: 3px;
`;

const Navigation = styled.div`
  background: #00338d;
  font-size: 3em;
  color: #fff;
  height: 64px;
  padding: 8px 16px 8px 8px;
  border: 2px solid black;
  border-radius: 3px;
`;

const FormDiv = styled.div`
  background: #00338d;
  display: flex;
  flex-direction: column;
  width: 256px;
  row-gap: 8px;
  align-items: center;
  justify-content: center;
`;

const Label = styled.div`
  background: #00338d;
  color: black;
  font-size: 1.1em;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
`;

export default { Button, Navigation, FormDiv, Label };
