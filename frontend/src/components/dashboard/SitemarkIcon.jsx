import * as React from "react";
import Box from "@mui/material/Box";
import logo from "../../assets/coco-bambu-logo.png";

export default function SitemarkIcon(props) {
  return (
    <Box
      component="img"
      src={logo}
      alt="Coco Bambu"
      sx={{
        height: 40,   // aumenta aqui
        width: "auto",
        display: "block",
      }}
      {...props}
    />
  );
}