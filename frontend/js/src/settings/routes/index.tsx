import * as React from "react";
import SettingsLayout from "../layout";
import DeleteAccount from "../delete/DeleteAccount";
import DeleteListens from "../delete-listens/DeleteListens";
import Export from "../export/ExportData";
import Import, { ImportLoader } from "../import/ImportListens";
import {
  MissingMBDataPageLoader,
  MissingMBDataPageWrapper as MissingMBDataPage,
} from "../missing-data/MissingMBData";
import MusicServices, {
  MusicServicesLoader,
} from "../music-services/details/MusicServices";
import ResetToken from "../resettoken/ResetToken";
import {
  SelectTimezoneLoader,
  SelectTimezoneWrapper as SelectTimezone,
} from "../select_timezone/SelectTimezone";
import {
  SelectTroiPreferencesLoader,
  SelectTroiPreferencesWrapper as SelectTroiPreferences,
} from "../troi/SelectTroiPreferences";
import Settings from "../Settings";
import ResetImportTimestamp from "../resetlatestimportts/ResetLatestImports";
import SelectArea, {
  SelectAreaLoader,
  SelectAreaWrapper,
} from "../select-location/SelectLocation";

const getSettingsRoutes = () => {
  const routes = [
    {
      path: "/settings",
      element: <SettingsLayout />,
      children: [
        {
          index: true,
          element: <Settings />,
        },
        {
          path: "resettoken/",
          element: <ResetToken />,
        },
        {
          path: "music-services/details/",
          loader: MusicServicesLoader,
          element: <MusicServices />,
        },
        {
          path: "import/",
          loader: ImportLoader,
          element: <Import />,
        },
        {
          path: "resetlatestimportts/",
          element: <ResetImportTimestamp />,
        },
        {
          path: "missing-data/",
          loader: MissingMBDataPageLoader,
          element: <MissingMBDataPage />,
        },
        {
          path: "select_timezone/",
          loader: SelectTimezoneLoader,
          element: <SelectTimezone />,
        },
        {
          path: "select-area/",
          loader: SelectAreaLoader,
          element: <SelectAreaWrapper />,
        },
        {
          path: "troi/",
          loader: SelectTroiPreferencesLoader,
          element: <SelectTroiPreferences />,
        },
        {
          path: "export/",
          element: <Export />,
        },
        {
          path: "delete-listens/",
          element: <DeleteListens />,
        },
        {
          path: "delete/",
          element: <DeleteAccount />,
        },
      ],
    },
  ];
  return routes;
};

export default getSettingsRoutes;
