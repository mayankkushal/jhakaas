import { makeStyles } from "@material-ui/core/styles";

export const useToolbarStyles = makeStyles(
  (theme) => ({
    toolbar: {
      backgroundColor:
        theme.palette.type === "light"
          ? theme.palette.grey[100]
          : theme.palette.grey[900],
    },
    desktopToolbar: {
      marginTop: theme.spacing(2),
    },
    mobileToolbar: {
      position: "fixed",
      bottom: 0,
      left: 0,
      right: 0,
      padding: "16px",
      width: "100%",
      boxSizing: "border-box",
      flexShrink: 0,
      zIndex: 2,
    },
    modal: {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    },
    paper: {
      backgroundColor: theme.palette.background.paper,
      border: "2px solid #000",
      boxShadow: theme.shadows[5],
      padding: theme.spacing(2, 4, 3),
    },
    defaultToolbar: {
      flex: 1,
      display: "flex",
      justifyContent: "space-between",
    },
    spacer: {
      [theme.breakpoints.down("xs")]: {
        height: "5em",
      },
    },
  }),
  { name: "RaToolbar" }
);
