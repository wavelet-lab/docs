@websdr/nestjs-microservice
===========================

Reusable NestJS building blocks for the WebSDR backend.

This package is published as an npm module and is intended to be **embedded into your NestJS app** (import modules, reuse guards/services), not run as a standalone server by itself.

What’s inside
-------------

-  **Auth** (``/auth``): ``AuthModule``, ``AuthService``, ``JwtAuthGuard``, DTOs and interfaces.
-  **Users** (``/users``): ``UsersModule`` and ``UsersService``.
-  **Common** (``/common``): a small logging helper module (``LoggingModule``, ``createContextLogger``) and ``LoggerLevelService``/``parseLogLevels``.

Install
-------

.. code:: bash

   npm install @websdr/nestjs-microservice

.. code:: bash

   pnpm add @websdr/nestjs-microservice

.. code:: bash

   yarn add @websdr/nestjs-microservice

Importing
---------

This package is published as ESM (see ``type: module``).

Import from the root:

.. code:: ts

   import { AuthModule, UsersModule, JwtAuthGuard } from '@websdr/nestjs-microservice';

Or use subpath exports:

.. code:: ts

   import { AuthModule, JwtAuthGuard } from '@websdr/nestjs-microservice/auth';
   import { UsersModule } from '@websdr/nestjs-microservice/users';
   import { LoggingModule, LOGGER } from '@websdr/nestjs-microservice/common';

Usage
-----

.. _1-import-modules-in-your-nest-app:

1) Import modules in your Nest app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ts

   import { Module } from '@nestjs/common';
   import { AuthModule, UsersModule } from '@websdr/nestjs-microservice';

   @Module({
     imports: [UsersModule, AuthModule],
   })
   export class AppModule {}

.. _2-protect-controllers-with-jwtauthguard:

2) Protect controllers with ``JwtAuthGuard``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``JwtAuthGuard`` validates a JWT (Passport strategy) and also checks token revocation via ``AuthService.isRevoked()``.
It looks for the token in either:

-  ``req.cookies.jwt``, or
-  ``Authorization: Bearer <token>``

.. code:: ts

   import { Controller, Get, UseGuards } from '@nestjs/common';
   import { JwtAuthGuard } from '@websdr/nestjs-microservice/auth';

   @Controller('private')
   export class PrivateController {
     @UseGuards(JwtAuthGuard)
     @Get()
     getPrivateData() {
       return { ok: true };
     }
   }

Accessing the authenticated user (``req.user``) with proper typing:

.. code:: ts

   import { Controller, Get, Req, UseGuards } from '@nestjs/common';
   import type { AuthRequest } from '@websdr/nestjs-microservice/auth';
   import { JwtAuthGuard } from '@websdr/nestjs-microservice/auth';

   @Controller('me')
   export class MeController {
     @UseGuards(JwtAuthGuard)
     @Get()
     getMe(@Req() req: AuthRequest) {
       return req.user;
     }
   }

.. _3-provide-a-logger-instance-via-loggingmodule:

3) Provide a logger instance via ``LoggingModule``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``LoggingModule.forRoot()`` registers a logger instance under the ``LOGGER`` token.
``createContextLogger()`` wraps a base logger and adds Nest-like context.

.. code:: ts

   import { Module, Logger } from '@nestjs/common';
   import { LoggingModule } from '@websdr/nestjs-microservice/common';

   @Module({
     imports: [LoggingModule.forRoot(new Logger())],
   })
   export class AppModule {}

Injecting the base logger and creating a context-aware wrapper:

.. code:: ts

   import { Inject, Injectable } from '@nestjs/common';
   import type { LoggerService } from '@nestjs/common';
   import { LOGGER, createContextLogger } from '@websdr/nestjs-microservice/common';

   @Injectable()
   export class DeviceService {
     private readonly logger: LoggerService;

     constructor(@Inject(LOGGER) base: any) {
       this.logger = createContextLogger(base, DeviceService.name);
     }

     open() {
       this.logger.log('opening device');
     }
   }

.. _4-configure-log-levels:

4) Configure log levels
~~~~~~~~~~~~~~~~~~~~~~~

``parseLogLevels()`` parses strings like ``"debug,warn,error"``, as well as ``"all"``/``"on"`` and ``"off"``/``"false"``.

.. code:: ts

   import { Logger } from '@nestjs/common';
   import { parseLogLevels } from '@websdr/nestjs-microservice/common';

   Logger.overrideLogger(parseLogLevels(process.env.LOG_LEVELS));

If you prefer a service that can update levels at runtime:

.. code:: ts

   import { NestFactory } from '@nestjs/core';
   import { LoggerLevelService } from '@websdr/nestjs-microservice/common';
   import { AppModule } from './app.module';

   const app = await NestFactory.create(AppModule);
   app.get(LoggerLevelService).setLevelsFromString(process.env.LOG_LEVELS);
   await app.listen(3000);

Public API (summary)
--------------------

-  **``@websdr/nestjs-microservice/auth``**:

   -  ``AuthModule``
   -  ``JwtAuthGuard``
   -  DTOs: ``LoginDto``
   -  Types: ``AuthUser``, ``AuthRequest``

-  **``@websdr/nestjs-microservice/users``**:

   -  ``UsersModule``

-  **``@websdr/nestjs-microservice/common``**:

   -  ``LoggingModule``, ``LOGGER``, ``createContextLogger``
   -  ``LoggerLevelService``, ``parseLogLevels``, ``LoggerLevels``

Compatibility notes
-------------------

-  **NestJS:** built against NestJS v11.
-  **TypeScript:** ships ``*.d.ts`` typings.
-  **ESM:** package is ESM. If your app is CommonJS, use a bundler/transpiler setup that supports ESM dependencies.

Development
-----------

From the repository root:

.. code:: bash

   npm install

From this package folder:

Build
~~~~~

.. code:: bash

   npm run build

Test
~~~~

.. code:: bash

   npm test

Source links
------------

This package publishes ``dist/`` to npm. Source is available in the GitHub repository:

-  Entry point: https://github.com/wavelet-lab/websdr/blob/main/packages/nestjs-microservice/src/index.ts
-  Auth exports: https://github.com/wavelet-lab/websdr/blob/main/packages/nestjs-microservice/src/auth/index.ts
-  Common exports: https://github.com/wavelet-lab/websdr/blob/main/packages/nestjs-microservice/src/common/index.ts
-  Users exports: https://github.com/wavelet-lab/websdr/blob/main/packages/nestjs-microservice/src/users/index.ts

Package folder (GitHub):
https://github.com/wavelet-lab/websdr/tree/main/packages/nestjs-microservice

License
-------

WebSDR is `MIT licensed <https://github.com/wavelet-lab/websdr/blob/main/LICENSE>`__
