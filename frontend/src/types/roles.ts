// frontend/src/types/roles.ts

export const enum RoleEnum {
  LEITOR = 'leitor',
  PROFESSOR = 'professor',
  BOLSISTA = 'bolsista',
  ADMIN = 'admin'
}

export interface RoleOption {
  value: RoleEnum;
  label: string;
}

export const ROLE_OPTIONS: RoleOption[] = [
  { value: RoleEnum.LEITOR, label: 'Leitor (Acesso a notícias)' },
  { value: RoleEnum.PROFESSOR, label: 'Professor (Publicação/Gerenciamento)' },
  { value: RoleEnum.BOLSISTA, label: 'Bolsista (Publicação de notícias)' }
];
