import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import prettierConfig from 'eslint-config-prettier'

export default [
  // Базовые JS правила
  js.configs.recommended,

  // Vue правила
  ...pluginVue.configs['flat/recommended'],

  // Prettier правила
  prettierConfig,

  // Пользовательские правила
  {
    files: ['**/*.{js,vue}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
    },
    rules: {
      // Vue правила
      'vue/multi-word-component-names': 'off',
      'vue/require-default-prop': 'off',
      'vue/html-self-closing': [
        'error',
        {
          html: {
            void: 'always',
            normal: 'always',
            component: 'always',
          },
          svg: 'always',
          math: 'always',
        },
      ],
      'vue/component-name-in-template-casing': ['error', 'PascalCase'],
      'vue/attribute-hyphenation': ['error', 'always'],
      'vue/v-on-style': ['error', 'shorthand'],
      'vue/v-bind-style': ['error', 'shorthand'],

      // Possible Errors
      'no-unused-vars': 'warn',
      'no-undef': 'error',

      // Best Practices
      eqeqeq: ['error', 'always'],
      'no-var': 'error',
      'prefer-const': 'error',
      'object-shorthand': 'error',
      'prefer-template': 'error',
      'no-duplicate-imports': 'error',

      // Stylistic
      quotes: ['error', 'single'],
      semi: ['error', 'never'],
      'comma-dangle': ['error', 'always-multiline'],
    },
  },

  // Игнорирование файлов
  {
    ignores: ['node_modules/', 'dist/', '*.min.js', 'coverage/', '.env', '.env.*', '!.env.example'],
  },
]
