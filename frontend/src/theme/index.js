import { createTheme } from "@material-ui/core/styles";
import merge from "lodash/merge";
import { defaultTheme } from "react-admin";

const palette = merge({}, defaultTheme.palette, {
  primary: {
    main: "#00ba00", // Not far from red
  },
  secondary: {
    main: "#ff0266", // Not far from green
  },
});

console.log(palette, defaultTheme);

const typography = {
  // fontFamilySecondary: "'Poppins', sans-serif",
  // fontFamily: '"Comic Neue", cursive',
  fontSize: 16, // Should be a number in pixels
  fontStyle: "normal",
  fontWeightLight: 400,
  fontWeightRegular: 500,
  fontWeightMedium: 600,
  fontWeightBold: 700,
  color: "black",
};

const typographyBase = {
  fontFamily: typography.fontFamily,
  fontSize: typography.fontSize,
  fontStyle: typography.fontStyle,
  color: typography.color,
};

const typographyHeader = {
  ...typographyBase,
  fontWeight: typography.fontWeightBold,
  fontFamily: typography.fontFamilySecondary, // Use a dedicated font for the header
};

const typographyBody = {
  ...typographyBase,
  fontWeight: typography.fontWeightRegular,
  fontFamily: typography.fontFamily,
};

const rawTheme = {
  palette,
  typography: {
    ...typographyBase,
    h1: {
      ...typographyHeader,
      textTransform: "uppercase",
      fontSize: "4rem",
    },
    // ... Put other title styles below
    body1: {
      ...typographyBody,
      fontSize: "1rem",
    },
  },
};

export const theme = createTheme(merge({}, defaultTheme, rawTheme));
