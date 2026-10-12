import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';

export const name = 'darkzone-refresh-dsh';
export const PACKAGE_NAME = '@iasi/darkzone-refresh-dsh';

export function resolveDarkzoneRefreshSkillRoot(profileBaseUrl) {
  if (!profileBaseUrl) {
    throw new Error('darkzone-refresh-dsh: missing DSH profile baseUrl for package resolution');
  }
  let manifestPath;
  try {
    manifestPath = createRequire(profileBaseUrl).resolve(`${PACKAGE_NAME}/package.json`);
  } catch (error) {
    throw new Error(
      `darkzone-refresh-dsh: cannot resolve ${PACKAGE_NAME}/package.json from the DSH profile`,
      { cause: error },
    );
  }
  return join(dirname(manifestPath), 'skills');
}
