import SettingsIcon from '@mui/icons-material/Settings';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const RoutesTitle = {
    '/home/upload-file': {
        title: 'Enviar arquivos'
    },
    '/home/operations': {
        title: 'Operações'
    }
}

const RoutesNavigation  = [
  {
    title: 'Enviar arquivos',
    href: '/home/upload-file',
    icon: CloudUploadIcon
  },
  {
    title: 'Operações',
    href: '/home/operations',
    icon: SettingsIcon
  }
];


export {
    RoutesTitle,
    RoutesNavigation
}
